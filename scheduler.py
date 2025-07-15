import schedule
import time
import threading
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from config import ReportConfig
from report_generator import ReportGenerator

class ReportScheduler:
    """Handles automatic scheduling and delivery of reports"""
    
    def __init__(self):
        self.config = ReportConfig()
        self.generator = ReportGenerator()
        self.logger = self._setup_logger()
        self.running = False
        
    def _setup_logger(self):
        """Setup logging for scheduler"""
        log_file = os.path.join(ReportConfig.LOGS_DIR, "scheduler.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def send_email_report(self, report_path, recipients=None):
        """Send report via email"""
        try:
            if recipients is None:
                recipients = self.config.EMAIL_SETTINGS['recipients']
            
            msg = MIMEMultipart()
            msg['From'] = self.config.EMAIL_SETTINGS['sender_email']
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = f"Automatic Report - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Email body
            body = f"""
            Dear Team,
            
            Please find attached the automatic report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
            
            This report contains:
            - System performance metrics
            - Sales analytics
            - User engagement data
            - Financial summary
            
            Best regards,
            Automatic Report System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach report file
            if report_path and os.path.exists(report_path):
                with open(report_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(report_path)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.config.EMAIL_SETTINGS['smtp_server'], 
                                self.config.EMAIL_SETTINGS['smtp_port'])
            server.starttls()
            server.login(self.config.EMAIL_SETTINGS['sender_email'], 
                        self.config.EMAIL_SETTINGS['sender_password'])
            
            text = msg.as_string()
            server.sendmail(self.config.EMAIL_SETTINGS['sender_email'], recipients, text)
            server.quit()
            
            self.logger.info(f"Report emailed successfully to {recipients}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False
    
    def generate_and_send_daily_report(self):
        """Generate daily report and send via email"""
        try:
            self.logger.info("Starting daily report generation...")
            
            # Generate PDF report
            report_path = self.generator.generate_comprehensive_report("pdf")
            
            if report_path:
                self.logger.info(f"Daily report generated: {report_path}")
                
                # Send via email if configured
                if self.config.EMAIL_SETTINGS['sender_email'] != "your_email@gmail.com":
                    self.send_email_report(report_path)
                else:
                    self.logger.info("Email not configured, report saved locally only")
            else:
                self.logger.error("Failed to generate daily report")
                
        except Exception as e:
            self.logger.error(f"Error in daily report generation: {e}")
    
    def generate_and_send_weekly_report(self):
        """Generate weekly report with Excel format"""
        try:
            self.logger.info("Starting weekly report generation...")
            
            # Generate Excel report for weekly summary
            report_path = self.generator.generate_comprehensive_report("excel")
            
            if report_path:
                self.logger.info(f"Weekly report generated: {report_path}")
                
                if self.config.EMAIL_SETTINGS['sender_email'] != "your_email@gmail.com":
                    self.send_email_report(report_path)
                else:
                    self.logger.info("Email not configured, report saved locally only")
            else:
                self.logger.error("Failed to generate weekly report")
                
        except Exception as e:
            self.logger.error(f"Error in weekly report generation: {e}")
    
    def generate_and_send_monthly_report(self):
        """Generate monthly comprehensive report with all formats"""
        try:
            self.logger.info("Starting monthly report generation...")
            
            # Generate all formats for monthly report
            pdf_path = self.generator.generate_comprehensive_report("pdf")
            excel_path = self.generator.generate_comprehensive_report("excel")
            html_path = self.generator.generate_comprehensive_report("html")
            
            generated_reports = [path for path in [pdf_path, excel_path, html_path] if path]
            
            if generated_reports:
                self.logger.info(f"Monthly reports generated: {len(generated_reports)} files")
                
                # Send the main PDF report
                if pdf_path and self.config.EMAIL_SETTINGS['sender_email'] != "your_email@gmail.com":
                    self.send_email_report(pdf_path)
                else:
                    self.logger.info("Email not configured, reports saved locally only")
            else:
                self.logger.error("Failed to generate monthly reports")
                
        except Exception as e:
            self.logger.error(f"Error in monthly report generation: {e}")
    
    def setup_schedules(self):
        """Setup all scheduled tasks"""
        try:
            # Daily report at 9:00 AM
            schedule.every().day.at(self.config.REPORT_SCHEDULE['daily']).do(
                self.generate_and_send_daily_report
            )
            
            # Weekly report every Monday at 9:00 AM
            schedule.every().monday.at("09:00").do(
                self.generate_and_send_weekly_report
            )
            
            # Monthly report on the 1st of each month at 9:00 AM
            schedule.every().month.do(
                self.generate_and_send_monthly_report
            )
            
            # Optional: Test report every 5 minutes (for demonstration)
            # Uncomment the line below to test scheduling
            # schedule.every(5).minutes.do(self.generate_and_send_daily_report)
            
            self.logger.info("All schedules setup successfully")
            
        except Exception as e:
            self.logger.error(f"Error setting up schedules: {e}")
    
    def run_scheduler(self):
        """Run the scheduler in a separate thread"""
        self.running = True
        self.setup_schedules()
        
        self.logger.info("Scheduler started. Waiting for scheduled tasks...")
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                self.logger.info("Scheduler interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)
    
    def start_scheduler_thread(self):
        """Start scheduler in background thread"""
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        self.logger.info("Scheduler started in background thread")
        return scheduler_thread
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        schedule.clear()
        self.logger.info("Scheduler stopped")
    
    def run_immediate_report(self, report_type="comprehensive", format_type="pdf"):
        """Generate report immediately for testing"""
        try:
            self.logger.info(f"Generating immediate {report_type} report in {format_type} format...")
            
            if report_type == "daily":
                self.generate_and_send_daily_report()
            elif report_type == "weekly":
                self.generate_and_send_weekly_report()
            elif report_type == "monthly":
                self.generate_and_send_monthly_report()
            else:
                report_path = self.generator.generate_comprehensive_report(format_type)
                if report_path:
                    self.logger.info(f"Immediate report generated: {report_path}")
                    return report_path
                else:
                    self.logger.error("Failed to generate immediate report")
                    
        except Exception as e:
            self.logger.error(f"Error generating immediate report: {e}")
            return None
    
    def get_next_scheduled_times(self):
        """Get information about next scheduled report times"""
        jobs_info = []
        for job in schedule.jobs:
            jobs_info.append({
                'job': str(job.job_func.__name__),
                'next_run': job.next_run,
                'interval': job.interval,
                'unit': job.unit
            })
        return jobs_info
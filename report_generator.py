import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os
import io
import base64
from config import ReportConfig
from data_collector import DataCollector
import logging

class ReportGenerator:
    """Generates automated reports in multiple formats"""
    
    def __init__(self):
        self.config = ReportConfig()
        self.collector = DataCollector()
        self.logger = self._setup_logger()
        self.config.create_directories()
        
    def _setup_logger(self):
        """Setup logging for report generation"""
        log_file = os.path.join(ReportConfig.LOGS_DIR, "report_generation.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def create_charts(self, data_dict):
        """Create charts for the report"""
        charts = {}
        
        try:
            plt.style.use('default')  # Use default style instead of seaborn-v0_8
            
            # Sales chart
            if 'sales_data' in data_dict and not data_dict['sales_data'].empty:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                
                sales_by_product = data_dict['sales_data'].groupby('product')['sales_amount'].sum()
                ax1.pie(sales_by_product.values, labels=sales_by_product.index, autopct='%1.1f%%')
                ax1.set_title('Sales by Product')
                
                sales_by_date = data_dict['sales_data'].groupby('date')['sales_amount'].sum()
                ax2.plot(sales_by_date.index, sales_by_date.values)
                ax2.set_title('Sales Trend Over Time')
                ax2.tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                chart_path = os.path.join(self.config.REPORTS_DIR, 'sales_chart.png')
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                charts['sales'] = chart_path
                plt.close()
            
            # User analytics chart
            if 'user_analytics' in data_dict and not data_dict['user_analytics'].empty:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                
                df = data_dict['user_analytics']
                ax1.plot(df['date'], df['active_users'], label='Active Users', marker='o')
                ax1.plot(df['date'], df['new_users'], label='New Users', marker='s')
                ax1.set_title('User Analytics')
                ax1.legend()
                ax1.tick_params(axis='x', rotation=45)
                
                ax2.bar(df['date'], df['page_views'])
                ax2.set_title('Page Views')
                ax2.tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                chart_path = os.path.join(self.config.REPORTS_DIR, 'analytics_chart.png')
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                charts['analytics'] = chart_path
                plt.close()
            
            # Financial chart
            if 'financial_data' in data_dict and not data_dict['financial_data'].empty:
                fig, ax = plt.subplots(1, 1, figsize=(12, 6))
                
                df = data_dict['financial_data']
                x = range(len(df))
                width = 0.35
                
                ax.bar([i - width/2 for i in x], df['revenue'], width, label='Revenue', alpha=0.8)
                ax.bar([i + width/2 for i in x], df['expenses'], width, label='Expenses', alpha=0.8)
                
                ax.set_xlabel('Month')
                ax.set_ylabel('Amount')
                ax.set_title('Revenue vs Expenses')
                ax.set_xticks(x)
                ax.set_xticklabels([d.strftime('%b %Y') for d in df['month']], rotation=45)
                ax.legend()
                
                plt.tight_layout()
                chart_path = os.path.join(self.config.REPORTS_DIR, 'financial_chart.png')
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                charts['financial'] = chart_path
                plt.close()
                
            self.logger.info(f"Created {len(charts)} charts successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating charts: {e}")
            
        return charts
    
    def generate_pdf_report(self, data_dict, filename=None):
        """Generate PDF report"""
        try:
            if filename is None:
                filename = self.config.get_report_filename("comprehensive", "pdf")
            
            filepath = os.path.join(self.config.REPORTS_DIR, filename)
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            
            # Create story for PDF content
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph(self.config.REPORT_TITLE, title_style))
            story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Create charts
            charts = self.create_charts(data_dict)
            
            # Add charts to PDF
            for chart_name, chart_path in charts.items():
                if os.path.exists(chart_path):
                    story.append(Paragraph(f"{chart_name.title()} Analysis", styles['Heading2']))
                    img = Image(chart_path, width=6*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 12))
            
            # Add data tables
            for data_name, df in data_dict.items():
                if not df.empty:
                    story.append(Paragraph(f"{data_name.replace('_', ' ').title()} Summary", styles['Heading2']))
                    
                    # Convert DataFrame to table data
                    table_data = [df.columns.tolist()]
                    for _, row in df.head(10).iterrows():  # Show only first 10 rows
                        table_data.append([str(val)[:20] for val in row.tolist()])
                    
                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    story.append(table)
                    story.append(Spacer(1, 20))
            
            # Build PDF
            doc.build(story)
            self.logger.info(f"PDF report generated: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error generating PDF report: {e}")
            return None
    
    def generate_excel_report(self, data_dict, filename=None):
        """Generate Excel report with multiple sheets"""
        try:
            if filename is None:
                filename = self.config.get_report_filename("comprehensive", "xlsx")
            
            filepath = os.path.join(self.config.REPORTS_DIR, filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Summary sheet
                summary_data = {
                    'Report Generated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                    'Company': [self.config.COMPANY_NAME],
                    'Total Data Sources': [len(data_dict)]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Data sheets
                for sheet_name, df in data_dict.items():
                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name.replace('_', ' ').title()[:31], index=False)
            
            self.logger.info(f"Excel report generated: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error generating Excel report: {e}")
            return None
    
    def generate_html_report(self, data_dict, filename=None):
        """Generate HTML report"""
        try:
            if filename is None:
                filename = self.config.get_report_filename("comprehensive", "html")
            
            filepath = os.path.join(self.config.REPORTS_DIR, filename)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{self.config.REPORT_TITLE}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    h1 {{ color: #333; text-align: center; }}
                    h2 {{ color: #666; border-bottom: 2px solid #666; padding-bottom: 5px; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    .chart {{ text-align: center; margin: 20px 0; }}
                    .timestamp {{ text-align: center; color: #888; }}
                </style>
            </head>
            <body>
                <h1>{self.config.REPORT_TITLE}</h1>
                <p class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            """
            
            # Add data tables
            for data_name, df in data_dict.items():
                if not df.empty:
                    html_content += f"<h2>{data_name.replace('_', ' ').title()}</h2>"
                    html_content += df.head(10).to_html(classes='data-table', escape=False)
            
            html_content += "</body></html>"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"HTML report generated: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error generating HTML report: {e}")
            return None
    
    def generate_comprehensive_report(self, output_format="pdf"):
        """Generate a comprehensive report with all data"""
        try:
            self.logger.info("Starting comprehensive report generation...")
            
            # Collect all data
            data_dict = self.collector.collect_all_data()
            
            # Generate report based on format
            if output_format.lower() == "pdf":
                return self.generate_pdf_report(data_dict)
            elif output_format.lower() == "excel":
                return self.generate_excel_report(data_dict)
            elif output_format.lower() == "html":
                return self.generate_html_report(data_dict)
            else:
                self.logger.error(f"Unsupported format: {output_format}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating comprehensive report: {e}")
            return None
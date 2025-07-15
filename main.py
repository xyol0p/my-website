#!/usr/bin/env python3
"""
Automatic Report System - Main Application
Created for comprehensive automated reporting
"""

import argparse
import sys
import os
import time
from datetime import datetime
from config import ReportConfig
from data_collector import DataCollector
from report_generator import ReportGenerator
from scheduler import ReportScheduler

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    AUTOMATIC REPORT SYSTEM                       ║
    ║                      Python-based Solution                       ║
    ║                                                                  ║
    ║  Features:                                                       ║
    ║  • Multi-format reports (PDF, Excel, HTML)                      ║
    ║  • Automatic scheduling (Daily, Weekly, Monthly)                ║
    ║  • Email delivery system                                        ║
    ║  • Data collection from multiple sources                        ║
    ║  • System metrics monitoring                                    ║
    ║  • Beautiful charts and visualizations                          ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def setup_environment():
    """Setup the application environment"""
    try:
        # Create necessary directories
        ReportConfig.create_directories()
        print("✓ Directory structure created")
        
        # Test imports
        import pandas as pd
        import matplotlib.pyplot as plt
        print("✓ Core dependencies available")
        
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ Setup error: {e}")
        return False

def show_system_status():
    """Show current system status"""
    print("\n" + "="*60)
    print("SYSTEM STATUS")
    print("="*60)
    
    # Check directories
    dirs_to_check = [
        ReportConfig.DATA_DIR,
        ReportConfig.REPORTS_DIR,
        ReportConfig.TEMPLATES_DIR,
        ReportConfig.LOGS_DIR
    ]
    
    for dir_path in dirs_to_check:
        exists = "✓" if os.path.exists(dir_path) else "✗"
        print(f"{exists} Directory: {dir_path}")
    
    # Check report files
    if os.path.exists(ReportConfig.REPORTS_DIR):
        reports = [f for f in os.listdir(ReportConfig.REPORTS_DIR) if f.endswith(('.pdf', '.xlsx', '.html'))]
        print(f"✓ Generated reports: {len(reports)}")
        
        if reports:
            print("   Recent reports:")
            for report in sorted(reports)[-3:]:  # Show last 3 reports
                print(f"   - {report}")
    
    print(f"✓ Configuration loaded: {ReportConfig.COMPANY_NAME}")
    print(f"✓ Default format: {ReportConfig.DEFAULT_REPORT_FORMAT}")

def generate_sample_report():
    """Generate a sample report for demonstration"""
    print("\n" + "="*60)
    print("GENERATING SAMPLE REPORT")
    print("="*60)
    
    try:
        generator = ReportGenerator()
        
        print("Collecting sample data...")
        collector = DataCollector()
        data_dict = collector.collect_all_data()
        
        print("Generating PDF report...")
        pdf_path = generator.generate_pdf_report(data_dict)
        
        print("Generating Excel report...")
        excel_path = generator.generate_excel_report(data_dict)
        
        print("Generating HTML report...")
        html_path = generator.generate_html_report(data_dict)
        
        generated_files = [f for f in [pdf_path, excel_path, html_path] if f]
        
        if generated_files:
            print(f"\n✓ Successfully generated {len(generated_files)} sample reports:")
            for file_path in generated_files:
                print(f"  • {file_path}")
            return True
        else:
            print("✗ Failed to generate sample reports")
            return False
            
    except Exception as e:
        print(f"✗ Error generating sample reports: {e}")
        return False

def run_scheduler_mode():
    """Run the application in scheduler mode"""
    print("\n" + "="*60)
    print("STARTING SCHEDULER MODE")
    print("="*60)
    
    try:
        scheduler = ReportScheduler()
        
        # Show scheduled times
        print("Scheduled report times:")
        print(f"• Daily reports: {ReportConfig.REPORT_SCHEDULE['daily']}")
        print(f"• Weekly reports: Every {ReportConfig.REPORT_SCHEDULE['weekly']}")
        print(f"• Monthly reports: Day {ReportConfig.REPORT_SCHEDULE['monthly']} of each month")
        
        print("\nPress Ctrl+C to stop the scheduler\n")
        
        # Start scheduler
        scheduler.run_scheduler()
        
    except KeyboardInterrupt:
        print("\n✓ Scheduler stopped by user")
    except Exception as e:
        print(f"✗ Scheduler error: {e}")

def run_interactive_mode():
    """Run the application in interactive mode"""
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    
    scheduler = ReportScheduler()
    
    while True:
        print("\nAvailable options:")
        print("1. Generate immediate report (PDF)")
        print("2. Generate immediate report (Excel)")
        print("3. Generate immediate report (HTML)")
        print("4. Start scheduler in background")
        print("5. Show system status")
        print("6. View recent reports")
        print("7. Test email configuration")
        print("8. Exit")
        
        try:
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == "1":
                print("Generating PDF report...")
                report_path = scheduler.run_immediate_report("comprehensive", "pdf")
                if report_path:
                    print(f"✓ PDF report generated: {report_path}")
                
            elif choice == "2":
                print("Generating Excel report...")
                report_path = scheduler.run_immediate_report("comprehensive", "excel")
                if report_path:
                    print(f"✓ Excel report generated: {report_path}")
                
            elif choice == "3":
                print("Generating HTML report...")
                report_path = scheduler.run_immediate_report("comprehensive", "html")
                if report_path:
                    print(f"✓ HTML report generated: {report_path}")
                
            elif choice == "4":
                print("Starting scheduler in background...")
                thread = scheduler.start_scheduler_thread()
                print("✓ Scheduler started in background")
                print("Use option 8 to exit and stop scheduler")
                
            elif choice == "5":
                show_system_status()
                
            elif choice == "6":
                if os.path.exists(ReportConfig.REPORTS_DIR):
                    reports = [f for f in os.listdir(ReportConfig.REPORTS_DIR) 
                              if f.endswith(('.pdf', '.xlsx', '.html'))]
                    if reports:
                        print(f"\nFound {len(reports)} reports:")
                        for report in sorted(reports):
                            file_path = os.path.join(ReportConfig.REPORTS_DIR, report)
                            size = os.path.getsize(file_path) / 1024  # KB
                            print(f"  • {report} ({size:.1f} KB)")
                    else:
                        print("No reports found")
                else:
                    print("Reports directory not found")
                
            elif choice == "7":
                print("Testing email configuration...")
                if ReportConfig.EMAIL_SETTINGS['sender_email'] == "your_email@gmail.com":
                    print("✗ Email not configured. Please update config.py with your email settings")
                else:
                    print(f"✓ Email configured for: {ReportConfig.EMAIL_SETTINGS['sender_email']}")
                    print(f"✓ Recipients: {ReportConfig.EMAIL_SETTINGS['recipients']}")
                
            elif choice == "8":
                print("Stopping scheduler and exiting...")
                scheduler.stop_scheduler()
                break
                
            else:
                print("Invalid option. Please select 1-8.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            scheduler.stop_scheduler()
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Automatic Report System - Python-based automated reporting solution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --sample          Generate sample reports
  python main.py --scheduler       Run in scheduler mode
  python main.py --interactive     Run in interactive mode
  python main.py --status          Show system status
        """
    )
    
    parser.add_argument('--sample', action='store_true', 
                       help='Generate sample reports and exit')
    parser.add_argument('--scheduler', action='store_true',
                       help='Run in automatic scheduler mode')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--status', action='store_true',
                       help='Show system status and exit')
    parser.add_argument('--setup', action='store_true',
                       help='Setup environment and exit')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Handle specific modes
    if args.setup:
        print("✓ Environment setup completed")
        return
    
    if args.status:
        show_system_status()
        return
    
    if args.sample:
        success = generate_sample_report()
        sys.exit(0 if success else 1)
    
    if args.scheduler:
        run_scheduler_mode()
        return
    
    if args.interactive:
        run_interactive_mode()
        return
    
    # Default behavior - interactive mode
    if len(sys.argv) == 1:
        print("Starting in interactive mode...")
        run_interactive_mode()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
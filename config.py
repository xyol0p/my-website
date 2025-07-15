import os
from datetime import datetime, timedelta

class ReportConfig:
    """Configuration settings for the automatic report system"""
    
    # File paths
    DATA_DIR = "data"
    REPORTS_DIR = "reports"
    TEMPLATES_DIR = "templates"
    LOGS_DIR = "logs"
    
    # Report settings
    DEFAULT_REPORT_FORMAT = "pdf"  # pdf, excel, html
    REPORT_TITLE = "Automatic System Report"
    COMPANY_NAME = "Your Company"
    
    # Data sources
    DATABASE_URL = "sqlite:///sample_data.db"
    API_ENDPOINTS = {
        "sales": "https://api.example.com/sales",
        "users": "https://api.example.com/users"
    }
    
    # Email settings (for automated delivery)
    EMAIL_SETTINGS = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your_email@gmail.com",
        "sender_password": "your_app_password",
        "recipients": ["recipient@example.com"]
    }
    
    # Schedule settings
    REPORT_SCHEDULE = {
        "daily": "09:00",
        "weekly": "monday",
        "monthly": 1  # day of month
    }
    
    # Chart settings
    CHART_STYLE = "seaborn-v0_8"
    CHART_DPI = 300
    CHART_SIZE = (10, 6)
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        for dir_path in [cls.DATA_DIR, cls.REPORTS_DIR, cls.TEMPLATES_DIR, cls.LOGS_DIR]:
            os.makedirs(dir_path, exist_ok=True)
    
    @classmethod
    def get_report_filename(cls, report_type="daily", format_type="pdf"):
        """Generate filename for reports"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{report_type}_report_{timestamp}.{format_type}"
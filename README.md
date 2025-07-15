# Automatic Report System (Python)

**एक स्वचालित रिपोर्ट सिस्टम** - A comprehensive Python-based automated reporting solution that generates beautiful reports in multiple formats with scheduling capabilities.

## 🚀 Features

- **Multiple Report Formats**: PDF, Excel, HTML
- **Automatic Scheduling**: Daily, Weekly, Monthly reports
- **Email Delivery**: Automatic email delivery of reports
- **Data Collection**: Multiple data sources (APIs, databases, CSV, system metrics)
- **Visual Charts**: Beautiful charts and visualizations using Matplotlib
- **System Monitoring**: Real-time system performance metrics
- **Configurable**: Easy configuration through config files
- **Interactive Interface**: Command-line interface with multiple modes

## 📋 Requirements

- Python 3.7+
- Required packages (install via requirements.txt)

## 🛠️ Installation

1. **Clone or download the system**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment**:
   ```bash
   python main.py --setup
   ```

## 🎯 Quick Start

### Generate Sample Reports
```bash
python main.py --sample
```

### Interactive Mode
```bash
python main.py --interactive
```

### Automatic Scheduler Mode
```bash
python main.py --scheduler
```

### Check System Status
```bash
python main.py --status
```

## 📊 Report Types

### 1. System Metrics Report
- CPU usage, memory usage, disk usage
- Network statistics
- System uptime information

### 2. Sales Analytics Report
- Sales by product analysis
- Sales trends over time
- Regional sales comparison
- Customer type analysis

### 3. User Analytics Report
- Active users tracking
- New user acquisition
- Page views analytics
- Session duration analysis

### 4. Financial Summary Report
- Revenue and expense tracking
- Profit analysis
- Growth rate calculations
- Monthly financial trends

## ⚙️ Configuration

### Basic Configuration
Edit `config.py` to customize:

```python
# Report settings
REPORT_TITLE = "Your Company Report"
COMPANY_NAME = "Your Company Name"
DEFAULT_REPORT_FORMAT = "pdf"  # pdf, excel, html

# Schedule settings
REPORT_SCHEDULE = {
    "daily": "09:00",
    "weekly": "monday",
    "monthly": 1
}
```

### Email Configuration
Update email settings in `config.py`:

```python
EMAIL_SETTINGS = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",
    "sender_password": "your_app_password",
    "recipients": ["recipient1@example.com", "recipient2@example.com"]
}
```

**Note**: For Gmail, use App Passwords instead of regular passwords.

## 📁 Project Structure

```
automatic-report-system/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── data_collector.py      # Data collection from various sources
├── report_generator.py    # Report generation in multiple formats
├── scheduler.py           # Automatic scheduling and email delivery
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── data/                 # Data storage directory
├── reports/              # Generated reports
├── templates/            # Report templates
└── logs/                 # Application logs
```

## 🔧 Usage Examples

### 1. Generate Immediate Reports

**PDF Report**:
```bash
python main.py --interactive
# Then select option 1
```

**Excel Report**:
```bash
python main.py --interactive
# Then select option 2
```

**HTML Report**:
```bash
python main.py --interactive
# Then select option 3
```

### 2. Start Automatic Scheduling

```bash
python main.py --scheduler
```

This will start the scheduler that automatically generates:
- Daily reports at 9:00 AM
- Weekly reports every Monday
- Monthly reports on the 1st of each month

### 3. Background Scheduling

```bash
python main.py --interactive
# Select option 4 to start scheduler in background
```

## 📈 Data Sources

### Supported Data Sources:
1. **System Metrics**: CPU, memory, disk usage via `psutil`
2. **Sample Data**: Generated sales, user analytics, and financial data
3. **Database**: SQLite database support
4. **APIs**: REST API data collection
5. **CSV Files**: Import data from CSV files

### Adding Custom Data Sources:

Extend the `DataCollector` class in `data_collector.py`:

```python
def collect_custom_data(self):
    """Add your custom data collection logic here"""
    # Your data collection code
    return pd.DataFrame(your_data)
```

## 📧 Email Setup

### Gmail Setup:
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password in `config.py`

### Other Email Providers:
Update SMTP settings in `config.py` according to your provider:

- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Use your provider's settings

## 🎨 Customization

### Custom Report Templates:
1. Create HTML templates in `templates/` directory
2. Modify `report_generator.py` to use custom templates

### Custom Charts:
Modify the `create_charts()` method in `report_generator.py`:

```python
def create_custom_chart(self, data):
    """Create custom visualization"""
    plt.figure(figsize=(12, 6))
    # Your chart code here
    plt.savefig('custom_chart.png')
```

### Custom Scheduling:
Add custom schedules in `scheduler.py`:

```python
# Custom schedule example
schedule.every().hour.do(self.generate_hourly_report)
schedule.every().friday.at("17:00").do(self.generate_weekly_summary)
```

## 🐛 Troubleshooting

### Common Issues:

1. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Permission Errors**:
   ```bash
   chmod +x main.py
   ```

3. **Email Sending Issues**:
   - Check email credentials
   - Verify SMTP settings
   - Ensure less secure app access is enabled (if required)

4. **Chart Generation Issues**:
   - Install additional matplotlib backends if needed
   - Check display environment variables

### Debug Mode:
Run with verbose logging:
```bash
python main.py --interactive
# Check logs in logs/ directory
```

## 📝 Logs

All activities are logged in the `logs/` directory:

- `data_collection.log`: Data collection activities
- `report_generation.log`: Report generation logs
- `scheduler.log`: Scheduling and email delivery logs

## 🔐 Security Notes

- Store email passwords securely
- Use environment variables for sensitive data
- Regularly update dependencies
- Implement proper access controls for generated reports

## 🚀 Advanced Features

### API Integration:
```python
# Add in data_collector.py
def collect_from_api(self, endpoint):
    response = requests.get(endpoint, headers=your_headers)
    return pd.json_normalize(response.json())
```

### Database Integration:
```python
# Database connection example
def collect_from_database(self, query):
    conn = sqlite3.connect('your_database.db')
    df = pd.read_sql_query(query, conn)
    return df
```

### Custom Filters:
```python
# Add data filtering
def filter_data_by_date(self, df, start_date, end_date):
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]
```

## 📞 Support

For questions or issues:

1. Check the logs in `logs/` directory
2. Review configuration in `config.py`
3. Test with sample data first
4. Verify all dependencies are installed

## 📄 License

This project is created for educational and business use. Feel free to modify and distribute according to your needs.

## 🙏 Acknowledgments

- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **ReportLab**: PDF generation
- **Schedule**: Task scheduling
- **psutil**: System monitoring

---

**Happy Reporting! 📊✨**

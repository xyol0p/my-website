import pandas as pd
import sqlite3
import requests
import psutil
import json
import os
from datetime import datetime, timedelta
from config import ReportConfig
import logging

class DataCollector:
    """Collects data from various sources for report generation"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """Setup logging for data collection"""
        ReportConfig.create_directories()
        log_file = os.path.join(ReportConfig.LOGS_DIR, "data_collection.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            metrics = {
                'timestamp': datetime.now(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'network_sent': psutil.net_io_counters().bytes_sent,
                'network_recv': psutil.net_io_counters().bytes_recv,
                'boot_time': datetime.fromtimestamp(psutil.boot_time())
            }
            self.logger.info("System metrics collected successfully")
            return pd.DataFrame([metrics])
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
            return pd.DataFrame()
    
    def collect_sample_sales_data(self):
        """Generate sample sales data for demonstration"""
        try:
            import random
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
            
            sales_data = []
            for date in dates[:30]:  # Last 30 days
                sales_data.append({
                    'date': date,
                    'product': random.choice(['Product A', 'Product B', 'Product C', 'Product D']),
                    'sales_amount': random.uniform(1000, 10000),
                    'quantity': random.randint(1, 100),
                    'region': random.choice(['North', 'South', 'East', 'West']),
                    'customer_type': random.choice(['New', 'Returning'])
                })
            
            self.logger.info("Sample sales data generated successfully")
            return pd.DataFrame(sales_data)
        except Exception as e:
            self.logger.error(f"Error generating sales data: {e}")
            return pd.DataFrame()
    
    def collect_user_analytics(self):
        """Generate sample user analytics data"""
        try:
            import random
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
            
            user_data = []
            for date in dates[:30]:  # Last 30 days
                user_data.append({
                    'date': date,
                    'new_users': random.randint(10, 100),
                    'active_users': random.randint(100, 1000),
                    'page_views': random.randint(500, 5000),
                    'session_duration': random.uniform(1, 10),  # minutes
                    'bounce_rate': random.uniform(0.1, 0.8)
                })
            
            self.logger.info("User analytics data generated successfully")
            return pd.DataFrame(user_data)
        except Exception as e:
            self.logger.error(f"Error generating user analytics: {e}")
            return pd.DataFrame()
    
    def collect_financial_summary(self):
        """Generate sample financial data"""
        try:
            current_month = datetime.now().replace(day=1)
            months = []
            for i in range(12):
                month_date = current_month - timedelta(days=30*i)
                months.append(month_date)
            
            financial_data = []
            for month in reversed(months):
                import random
                revenue = random.uniform(50000, 150000)
                expenses = random.uniform(30000, 100000)
                
                financial_data.append({
                    'month': month,
                    'revenue': revenue,
                    'expenses': expenses,
                    'profit': revenue - expenses,
                    'growth_rate': random.uniform(-0.1, 0.3)
                })
            
            self.logger.info("Financial data generated successfully")
            return pd.DataFrame(financial_data)
        except Exception as e:
            self.logger.error(f"Error generating financial data: {e}")
            return pd.DataFrame()
    
    def collect_from_database(self, query, db_path=None):
        """Collect data from SQLite database"""
        try:
            if db_path is None:
                db_path = ReportConfig.DATABASE_URL.replace('sqlite:///', '')
            
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            self.logger.info(f"Data collected from database: {len(df)} rows")
            return df
        except Exception as e:
            self.logger.error(f"Error collecting from database: {e}")
            return pd.DataFrame()
    
    def collect_from_api(self, endpoint, headers=None):
        """Collect data from API endpoint"""
        try:
            response = requests.get(endpoint, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            df = pd.json_normalize(data)
            
            self.logger.info(f"Data collected from API: {len(df)} rows")
            return df
        except Exception as e:
            self.logger.error(f"Error collecting from API: {e}")
            return pd.DataFrame()
    
    def collect_from_csv(self, file_path):
        """Collect data from CSV file"""
        try:
            df = pd.read_csv(file_path)
            self.logger.info(f"Data collected from CSV: {len(df)} rows")
            return df
        except Exception as e:
            self.logger.error(f"Error collecting from CSV: {e}")
            return pd.DataFrame()
    
    def collect_all_data(self):
        """Collect data from all sources"""
        self.logger.info("Starting comprehensive data collection...")
        
        data_sources = {
            'system_metrics': self.collect_system_metrics(),
            'sales_data': self.collect_sample_sales_data(),
            'user_analytics': self.collect_user_analytics(),
            'financial_data': self.collect_financial_summary()
        }
        
        self.logger.info("All data collection completed")
        return data_sources
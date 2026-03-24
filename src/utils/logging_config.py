"""Logging and monitoring configuration"""
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configuration
LOG_LEVEL = logging.INFO
LOG_FILE = LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging():
    """Configure logging for the application"""
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (rotating)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(LOG_LEVEL)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    return root_logger


# Get logger instance
logger = setup_logging()


class MetricsCollector:
    """Collect API and application metrics"""
    
    def __init__(self):
        self.metrics = {
            "total_recommendations": 0,
            "total_analyses": 0,
            "total_errors": 0,
            "average_response_time": 0,
            "api_calls": {
                "recommend": 0,
                "analyze": 0,
                "preferences": 0,
                "history": 0
            }
        }
    
    def record_recommendation(self):
        """Record a recommendation call"""
        self.metrics["total_recommendations"] += 1
        self.metrics["api_calls"]["recommend"] += 1
        logger.info("Recommendation recorded")
    
    def record_analysis(self):
        """Record an analysis call"""
        self.metrics["total_analyses"] += 1
        self.metrics["api_calls"]["analyze"] += 1
        logger.info("Analysis recorded")
    
    def record_error(self, error_type: str):
        """Record an error"""
        self.metrics["total_errors"] += 1
        logger.error(f"Error recorded: {error_type}")
    
    def get_metrics(self):
        """Get current metrics"""
        return self.metrics


# Global metrics instance
metrics = MetricsCollector()


def log_api_call(endpoint: str, user_id: str = "anonymous", status: str = "success"):
    """Log API call"""
    logger.info(f"API Call: {endpoint} | User: {user_id} | Status: {status}")


def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)
    metrics.record_error(context)

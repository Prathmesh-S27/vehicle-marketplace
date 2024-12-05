import logging
from logging.handlers import RotatingFileHandler
import sys
from ..core.config import settings

def setup_logger():
    """
    Configure and return a logger
    """
    # Create logger
    logger = logging.getLogger('vehicle_marketplace')
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Create formatters
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File Handler (if log file is specified)
    if settings.LOG_FILE:
        file_handler = RotatingFileHandler(
            settings.LOG_FILE, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger

# Global logger instance
logger = setup_logger()

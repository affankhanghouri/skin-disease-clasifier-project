import logging
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime
import time
import os

# Constants for log configuration
LOG_DIR = 'logs'
# Use Windows-safe timestamp with epoch seconds for uniqueness
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M')}_{int(time.time())}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Keep last 3 logs

# Construct log file path
log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)
log_file_path = os.path.join(log_dir_path, LOG_FILE)


def configure_logger():
    """
    Configures logging with a rotating file handler and console handler.
    Avoids duplicate handlers if called multiple times.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Define formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Configuring logger immediately when this module is imported
logger = configure_logger()


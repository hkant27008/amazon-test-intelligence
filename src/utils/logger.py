# src/utils/logger.py
"""
Logger configuration for the test framework
Provides consistent logging across all components
"""

import logging
import sys
from datetime import datetime
import os

def setup_logger(name: str = "AmazonTest") -> logging.Logger:
    """
    Set up logger with console and file handlers
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only add handlers if they don't exist
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler
        log_dir = os.path.join("reports", "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(
            log_dir, 
            f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

# Create a default logger instance
logger = setup_logger()
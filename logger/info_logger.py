import logging
from datetime import datetime
import os

def info_logger():
    logger = logging.getLogger("info_logger")
    logger.setLevel(logging.INFO)
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'info_logs.log')
    fh = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(fh)
    
    return logger
import logging
from datetime import datetime
import os

def llm_cost_logger():
    cost_logger = logging.getLogger("llm_cost_logger")
    cost_logger.setLevel(logging.INFO)
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'llm_cost_logs.log')
    cost_fh = logging.FileHandler(log_path)
    cost_formatter = logging.Formatter('%(asctime)s %(message)s')
    cost_fh.setFormatter(cost_formatter)
    if not cost_logger.hasHandlers():
        cost_logger.addHandler(cost_fh)

    return cost_logger

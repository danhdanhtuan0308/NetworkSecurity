import logging 
import os 
from datetime import datetime 
"""
This module is used to create a logger object that can be used to log messages to a file.
"""
LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y_%H_%M_%S')}.log"

# Define the logs directory (not the full file path yet)
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)


#Log config 
logging.basicConfig(
    filename= LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
    )

logger = logging.getLogger("NetworkSecurityLogger")

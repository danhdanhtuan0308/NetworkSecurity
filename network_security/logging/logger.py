import logging 
import os 
from datetime import datetime 
"""
This module is used to create a logger object that can be used to log messages to a file.
"""
LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y_%H_%M_%S')}.log"

logs_path = os.path.join(os.getcwd(),'logs',LOG_FILE)
os.makedirs(logs_path , exist_ok=True)

LOG_FILE_PATh = os.path.join(logs_path, LOG_FILE)

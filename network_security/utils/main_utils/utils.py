import yaml 
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import os, sys
import numpy as np
import pickle

import dill 

#Read the yaml files 
def read_yaml_file(file_path:str) -> dict: 
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
#Write the yaml files
def write_yaml_file(file_path : str, content : object , replace : bool = False) -> None : 
    try : 
        if replace : 
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

#Copy numpy array data 
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
# Save object to file
def save_object(file_path: str, obj: object) -> None:
    """
    Save a Python object to a file using pickle
    file_path: str location of file to save
    obj: object to save
    """
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

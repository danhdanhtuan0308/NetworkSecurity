from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json 
import sys
import certifi 
import pandas as pd
import numpy as np
import pymongo
from network_security.exception.exception import NetworkSecurityException 
from network_security.logging.logger import logger

# Load environment variables from the .env file
load_dotenv()
#Establish a connection to the MongoDB server
uri = os.getenv("MONGO_DB_URL")


ca = certifi.where()
class NetworkDataExtract(): 
    def __init__(self):
        try:
            pass 
        except Exception as e: 
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection): 
        try: 
            self.data = database 
            self.collection = collection 
            self.records = records 

            self.mongo_client = pymongo.MongoClient(uri)
            self.database = self.mongo_client[self.data] 
            self.collection = self.database[self.collection]
            self.collection.insert_many(records)

            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == "__main__": 
    FILE_PATH = "network_data/phisingData.csv"
    DATABASE = "NetworkData"
    COLLECTION = "PhisingData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json(file_path= FILE_PATH)
    no_records = networkobj.insert_data_mongodb(records,DATABASE,COLLECTION)
    print(f"Number of records inserted: {no_records}")
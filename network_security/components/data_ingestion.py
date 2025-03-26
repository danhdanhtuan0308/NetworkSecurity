from network_security.exception.exception import NetworkSecurityException 
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact
import os 
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split 

from dotenv import load_dotenv 
load_dotenv()

"""
Initalize the data ingestion from the MongoDB server
"""


#Connect to the MongoDB server
MONGO_DB_URL = os.getenv("MONGO_DB_URL") 

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            #Get the data ingestion configuration
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_collection_as_df(self):
        try:
            # Connect to the MongoDB server
            database_name = self.data_ingestion_config.database_name
            # Get the collection name
            collection_name = self.data_ingestion_config.collection_name
            # Establish a connection to the MongoDB server
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection_name = self.mongo_client[database_name][collection_name]
            # Export the collection as a dataframe
            df = pd.DataFrame(list(collection_name.find()))
            if "_id" in list(df.columns):  # Fix: Convert columns to a list
                df = df.drop(columns=["_id"], axis=1)
            
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
            
    #Export data to the feature store    
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #Create folder 
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index = False,header = True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    #Perform train test split
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            #Get the train test split ratio
            train_set, test_set = train_test_split(dataframe, test_size= self.data_ingestion_config.train_test_split_ratio ) 
            logging.info(f"perform train test split on DF ")
            logging.info(f"Exited split_data_as_train_test method of Data Ingestion")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Exporting train test file")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index = False,header = True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index = False,header = True)
            logging.info(f"successfully exported train test file")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_df()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_aritifact = DataIngestionArtifact(
                trained_file_path = self.data_ingestion_config.training_file_path,
                test_file_path = self.data_ingestion_config.testing_file_path,
            )
            return data_ingestion_aritifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)
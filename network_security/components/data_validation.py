from network_security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from network_security.entity.config_entity import DataIngestionConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.constant.training_pipeline import SCHEMA_FILE_PATH 
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataIngestionConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Reqired number of columns: {number_of_columns}")
            logging.info(f"Actual number of columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_data_drift(self,base_df , current_df, threshold = 0.05 )->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                sample_distance = ks_2samp(d1,d2)
                if threshold <= sample_distance.pvalue:
                    is_found = False
                    report[column] = sample_distance
                else:
                    is_found = True
                    status = False
                
                report.update({
                    column:{
                        "p_value":float(sample_distance.pvalue),
                        "drift_status":is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            #Create directory 
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path= drift_report_file_path,content= report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self) -> DataValidationArtifact: 
        try:
            # Initialize error_message
            error_message = ""

            # Create train / test file path
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read the data
            train_data_frame = DataValidation.read_data(train_file_path)
            test_data_frame = DataValidation.read_data(test_file_path)

            # Validate the number of columns
            status = self.validate_number_of_columns(dataframe=train_data_frame)
            if not status: 
                error_message = f"{error_message} train data frame has incorrect number of columns"

            # For test data
            status = self.validate_number_of_columns(dataframe=test_data_frame)
            if not status: 
                error_message = f"{error_message} test data frame has incorrect number of columns"

            # Validate if the numerical columns exist
            numerical_columns = self._schema_config["numerical_columns"]
            for column in numerical_columns:
                if column not in train_data_frame.columns:
                    error_message = f"{error_message} {column} not found in train data frame"
                if column not in test_data_frame.columns:
                    error_message = f"{error_message} {column} not found in test data frame"

            # Check data drift
            status = self.detect_data_drift(base_df=train_data_frame, current_df=test_data_frame)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_data_frame.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_data_frame.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                validation_train_file_path=self.data_validation_config.valid_train_file_path,
                validation_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
)
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

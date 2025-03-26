import sys 
import os 
import numpy as np 
import pandas as pd 
from sklearn.impute import KNNImputer 
from sklearn.pipeline import Pipeline


from network_security.constant.training_pipeline import TARGET_COLUMN 
from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from network_security.entity.artifact_entity import ( 
    DataTransformationArtiact,
    DataValidationArtifact
)

from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException 
from network_security.logging.logger import logging 
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation: 
    def __init__(self,data_validation_artifact:DataTransformationArtiact,
                 data_transformation_config : DataTransformationConfig):
        try : 
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact 
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e : 
            raise NetworkSecurityException(e,sys)
        
    #Read the data   
    @staticmethod 
    def read_data(file_path) -> pd.DataFrame : 
        try : 
            return pd.read_csv(file_path)
        except Exception as e : 
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformer_object(cls) -> Pipeline:
        logging.info("Enter get_data_transformer_object of transformers class")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialized KNNImputer with params: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initate_data_transformation(self)-> DataTransformationArtiact : 
        logging.info("Enter data transformation method of the transformation class ")
        try : 
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.validation_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.validation_test_file_path)

            #training dataframe 
            input_feature_train_df = train_df.drop(columns= [TARGET_COLUMN], axis = 1)
            target_feature_train_df = train_df[TARGET_COLUMN] 
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            #testing dataframe 
            input_feature_test_df = test_df.drop(columns= [TARGET_COLUMN], axis = 1)
            target_feature_test_df = test_df[TARGET_COLUMN] 
            target_feature_test_df = target_feature_test_df.replace(-1,0)


            preprocessor= self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df) 

            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            # Save numpy array data
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path, array=train_arr
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path, array=test_arr
            )
            save_object(
                self.data_transformation_config.transformed_object_file_path, preprocessor_object
            )

            #Prep artifact 
            data_transformation_artifact = DataTransformationArtiact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact

        except Exception as e : 
            raise NetworkSecurityException(e,sys)
        

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        
        #Data Ingestion pipeline
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initialize the data ingestion process")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion process completed")
        print(data_ingestion_artifact)

        #Data Validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initialize the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation process completed")
        print(data_validation_artifact)

        #Data Transformation 
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("Initialize the data transformation process")
        data_transformation_artifact = data_transformation.initate_data_transformation()
        logging.info("Data transformation process completed")
        print(data_transformation_artifact)


    except Exception as e:
        raise NetworkSecurityException(e,sys)
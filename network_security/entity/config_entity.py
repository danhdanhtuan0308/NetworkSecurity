from datetime import datetime 
import os 
from network_security.constant import training_pipeline



class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        #Adjust timeframe format in the dir 
        timestamp = timestamp.strftime('%m-%d-%Y_%H_%M_%S')
        #Define the pipeline name and artifacts name
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifacts_name = training_pipeline.ARTIFACTS_DIR
        self.artifacts_dir = os.path.join(self.artifacts_name,timestamp)
        self.timestamp : str = timestamp

#Directory for storing the data ingestion (train.csv, test.csv) and feature store
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Use the artifacts_dir from the TrainingPipelineConfig object
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifacts_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILENAME
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

##Validtion 

class DataValidationConfig:
    def __init__ (self,training_pipeline_config : TrainingPipelineConfig):
        self.data_validation_dir : str = os.path.join(
            training_pipeline_config.artifacts_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        #Valid data
        self.valid_data_dir : str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )
        #Invalid data
        self.invalid_data_dir : str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )
        #Valid train
        self.valid_train_file_path : str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )
        #Valid test
        self.valid_test_file_path : str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )
        #Invalid train
        self.invalid_train_file_path : str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )
        #Invalid test
        self.invalid_test_file_path : str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )


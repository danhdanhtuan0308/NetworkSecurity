import os 
import sys
import pandas as pd
import numpy as np

"""
DEfine the constant variable for training pipeline 
"""

TARGET_COLUMN = "Result"
PIPELINE_NAME : str = "NetworkSecurity"
ARTIFACTS_DIR : str = "Artifacts"
FILENAME : str = "phisingData.csv"

TRAIN_FILE_NAME : str = "train.csv"
TEST_FILE_NAME : str = "test.csv"

"""
Data Ingestion Entity reated constant start with DATA_INGESTION var name
"""
DATA_INGESTION_COLLECTION_NAME: str = "PhisingData"
DATA_INGESTION_DATABASE_NAME: str = "NetworkData"
DATA_INGESTION_DIR_NAME : str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION : float = 0.2


"""
Data validation
"""

DATA_VALIDATION_DIR_NAME : str = "data_validation"
DATA_VALIDATION_VALID_DIR : str = "validated"
DATA_VALIDATION_INVALID_DIR : str = "invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"


SCHEMA_FILE_PATH: str = os.path.join("data_schema", "schema.yaml")
SAVE_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"
"""
Data transformation related to constant startwith Data_transformation
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"


#KNN imputer to replace nan values 
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,  # Correct parameter for missing values
    "n_neighbors": 3,          # Number of neighbors to use
    "weights": "uniform"       # Correct parameter for weights
}

DATA_TRANSFORMATION_TRAIN_FILE_PATH : str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH : str = "test.npy"

"""
Model trainer realated constant start with Mode Trainer Var name
"""

MODEL_NAME_DIR_NAME : str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "train_model"
MODEL_TRAINER_TRAINED_MODEL_NAME : str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE : float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05 
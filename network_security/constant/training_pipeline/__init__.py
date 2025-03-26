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


SCHEMA_FILE_PATH: str = os.path.join("data_schema", "schema.yaml")
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    validation_train_file_path: str
    validation_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


@dataclass
class DataTransformationArtiact:
    transformed_object_file_path: str
    transformed_train_file_path : str 
    transformed_test_file_path : str

@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision: float  
    recall: float

@dataclass
class ModelTrainerArtifact : 
    trained_model_file_path : str 
    train_metric_artifact : ClassificationMetricArtifact 
    test_metric_artifact : ClassificationMetricArtifact
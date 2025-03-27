import pandas as pd 
import numpy as np 
import os 
import sys 
from network_security.exception.exception import NetworkSecurityException 
from network_security.logging.logger import logging
from network_security.entity.artifact_entity import DataTransformationArtiact,ModelTrainerArtifact 
from network_security.entity.config_entity import ModelTrainerConfig 
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.main_utils.utils import save_object,load_object
from network_security.utils.main_utils.utils import load_numpy_array_data , evaluate_models
from network_security.utils.ml_utils.metric.classification_metric import  get_classification_score 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow


class ModelTrainer : 
    def __init__(self,model_trainer_config : ModelTrainerConfig,data_transformation_artifact:DataTransformationArtiact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e : 
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_models,classificationmetrics):
        with mlflow.start_run():
            f1_score = classificationmetrics.f1_score 
            precision = classificationmetrics.precision
            recall = classificationmetrics.recall

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision)
            mlflow.log_metric("recall",recall)
            mlflow.sklearn.log_model(best_models,"model")

    def train_model(self,X_train,y_train,x_test,y_test):
        models = {
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forrest": RandomForestClassifier(verbose=1),
            "Gradient Boosting": GradientBoostingClassifier(verbose= 1),
            "Logistic Regression" : LogisticRegression(verbose= 1),
            "AdaBoost": AdaBoostClassifier(),
        }
        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                'splitter': ['best', 'random'],
                # 'max_features': ['sqrt', 'log2'],
            },
            "Random Forrest": {
                # 'criterion': ['gini', 'entropy', 'log_loss'],
                'max_features': ['sqrt', 'log2'],
                'n_estimators': [ 128, 256],
            },
            "Gradient Boosting": {
                'loss': ['log_loss', 'exponential'],
                'learning_rate': [.1, .01, .05],
                'subsample': [0.6, 0.7, 0.75,0.9],
                # 'criterion': ['squared_error', 'friedman_mse'],
                'max_features': ['auto', 'sqrt', 'log2'],
                'n_estimators': [128, 256],
            },
            "Logistic Regression": {},
            "AdaBoost": {
                'learning_rate': [.1, .01, 0.5],
                'n_estimators': [128, 256],
            }
        }
        model_report: dict = evaluate_models(X_train = X_train, y_train = y_train , X_test= x_test , y_test = y_test,
                                            models = models , param= params )
        best_model_score = max(sorted(model_report.values()))
        #best Model
        best_mode_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_models = models[best_mode_name]
        y_train_pred = best_models.predict(X_train)

        classifiction_train_metrics = get_classification_score(y_true= y_train, y_pred = y_train_pred)
        #Track MLflow 

        self.track_mlflow(best_models,classifiction_train_metrics)


        y_test_pred = best_models.predict(x_test)
        classification_test_metric = get_classification_score(y_true= y_test, y_pred= y_test_pred)
        self.track_mlflow(best_models,classification_test_metric)

        preprocessor = load_object(file_path= self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok= True)

        #Save the Network model
        Network_Model = NetworkModel(preprocess= preprocessor , model = best_models)
        save_object(self.model_trainer_config.trained_model_file_path,obj = Network_Model)

        #Model Trainer artifact 
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact= classifiction_train_metrics, 
                             test_metric_artifact= classification_test_metric)
        
        logging.info(f'Model trainer artifact{model_trainer_artifact}')
        return model_trainer_artifact

    def initiate_model_trainer(self)->ModelTrainerArtifact: 
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

        # Loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_artifact = self.train_model(x_train,y_train,x_test,y_test)
            return model_artifact 


        except Exception as e : 
            raise NetworkSecurityException(e,sys)
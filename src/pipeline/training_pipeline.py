import os
import sys
from src.logger.logger import logging
from src.exception.exception import CustomException
import pandas as pd

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


# obj=DataIngestion()

# train_data_path,test_data_path=obj.initiate_data_ingestion()

# data_transformation=DataTransformation()

# train_arr,test_arr=data_transformation.initialize_data_transformation(train_data_path,test_data_path)


# model_trainer_obj=ModelTrainer()
# model_trainer_obj.initate_model_training(train_arr,test_arr)

# model_eval_obj = ModelEvaluation()
# model_eval_obj.initiate_model_evaluation(train_arr,test_arr)


class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion=DataIngestion()
            train_data_path,test_data_path=data_ingestion.initiate_data_ingestion()
            return train_data_path,test_data_path
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self,train_data_path,test_data_path):
        try:
            data_transformation=DataTransformation()

            train_arr,test_arr=data_transformation.initialize_data_transformation(train_data_path,test_data_path)
            return train_arr,test_arr
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_trainer(self, train_arr,test_arr):
        try:
            model_trainer_obj=ModelTrainer()
            model_trainer_obj.initate_model_training(train_arr,test_arr)
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_model_evaluation(self, train_arr,test_arr):
        try:
            model_eval_obj = ModelEvaluation()
            model_eval_obj.initiate_model_evaluation(train_arr,test_arr)
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_pipeline(self):
        try:
            train_data_path,test_data_path=self.start_data_ingestion()
            train_arr,test_arr=self.start_data_transformation(train_data_path,test_data_path)
            self.start_model_trainer(train_arr,test_arr)
            self.start_model_evaluation(train_arr,test_arr)
        except Exception as e:
            raise CustomException(e, sys)
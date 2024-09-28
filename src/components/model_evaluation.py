import numpy as np
from src.logger.logger import logging
from src.exception.exception import CustomException
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os
import sys
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import pickle
from src.utils.utils import load_object
from dataclasses import dataclass

@dataclass
class ModelEvaluationConfig:
    pass

class ModelEvaluation:
    def __init__(self):
        pass

    def initiate_model_evaluation(self):
        try:
            pass
        except Exception as e:
            logging.info(e)
            raise CustomException(e, sys)
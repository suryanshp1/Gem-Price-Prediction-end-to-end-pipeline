import pandas as pd
import numpy as np
from src.logger.logger import logging
from src.exception.exception import CustomException

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from sklearn.impute import SimpleImputer ## Handling missing value
from sklearn.preprocessing import StandardScaler ## Handling feature scaling
from sklearn.preprocessing import OrdinalEncoder ## Handling categorical features encoding
from sklearn.pipeline import Pipeline # Handling pipeline
from sklearn.compose import ColumnTransformer
from src.utils.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def initiate_data_transformation(self):
        try:
            pass
        except Exception as e:
            logging.info(e)
            raise CustomException(e, sys)
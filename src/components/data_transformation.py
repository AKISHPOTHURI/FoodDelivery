from dataclasses import dataclass
import numpy as np
import pandas as pd
import sys
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import data_Cleaning, save_object,calc_distance,sum
# from src.utils import calc_distance
import os

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            # logging.info("Data Transformation initiated")
            #categorical_cols
            categorical_cols = ['Weather_conditions', 'Road_traffic_density', 'Type_of_order','Type_of_vehicle', 'Festival', 'City', 'day_quaters']
            #numerical_cols
            numerical_cols = ['Delivery_person_Age', 'Delivery_person_Ratings', 'Restaurant_latitude','Restaurant_longitude', 
                              'Delivery_location_latitude','Delivery_location_longitude', 'Vehicle_condition','multiple_deliveries']
            #Nuerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
                ]
            )

            #Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('OrdinalEncoder', OrdinalEncoder()),
                ('scaler', StandardScaler())
                ]
            )
            #preprocessor
            preprocessor = ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_cols),
                ('cat_pipeline',cat_pipeline,categorical_cols)
            ])
            logging.info('data pipeline completed')
            return preprocessor

        except Exception as e:
            # logging.info("Error in Data Transformation")
            raise CustomException(e,sys)
    
    def initaite_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            #data cleaning
            train_df = data_Cleaning(train_df)
            test_df = data_Cleaning(test_df)
            #distance calculation
            train_df = calc_distance(train_df)
            test_df = calc_distance(test_df)

            train_df = train_df.dropna()
            test_df = test_df.dropna()
            # logging.info(test_df)
            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'Time_taken (min)'
            drop_columns = target_column_name

            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]

            # Trnasformating using preprocessor obj
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            # logging.info("Applying preprocessing object on training and testing datasets.")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )


        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")
            raise CustomException(e,sys)
        
# if __name__ == "__main__":
#     a = sum(5,4)
#     logging.info(a)
#     data_transformation = DataTransformation()
#     train_arr, test_arr,_ = data_transformation.initaite_data_transformation(train_data, test_data)
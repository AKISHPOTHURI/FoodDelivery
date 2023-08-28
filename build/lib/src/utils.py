import os
import pickle
import sys
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


def sum(a,b):
    return a+b

def data_Cleaning(df):
    try:
        
        logging.info("Data Cleaning as started")
        data=df.drop(labels=['ID','Delivery_person_ID'], axis=1)
        df = data.loc[data.isnull().sum(1)>=3]
        data = pd.concat([data, df, df]).drop_duplicates(keep=False)
        df = data[data['City'].notna()]
        for i in df.index:
            if df['Time_Orderd'][i] >= '05:00' and df['Time_Orderd'][i] < '10:00':
                df.loc[i,'day_quaters'] = 'morning'
            elif df['Time_Orderd'][i] >= '10:00' and df['Time_Orderd'][i] < '14:00':
                df.loc[i,'day_quaters'] = 'late morning'
            elif df['Time_Orderd'][i] >= '14:00' and df['Time_Orderd'][i] < '19:00':
                df.loc[i,'day_quaters'] = 'afternoon'
            elif df['Time_Orderd'][i] >= '19:00':
                df.loc[i,'day_quaters'] = 'night'
        df=df.drop(labels=['Time_Orderd','Time_Order_picked','Order_Date'], axis=1)
        df['Festival'].fillna("No", inplace = True) # 98% of the column has No as a value 
        df['day_quaters'].fillna("night", inplace = True) # most of the people ordered at night
        df['Delivery_person_Ratings'].fillna(round(np.mean(df['Delivery_person_Ratings']),1), inplace = True)
        df['Delivery_person_Age'].fillna(round(np.mean(df['Delivery_person_Age'])), inplace = True)
        df['multiple_deliveries'].fillna(round(np.mean(df['multiple_deliveries'])), inplace=True)
        df = df.dropna()
        logging.info('data cleaning ended')
        return df
    except Exception as e:
        logging.info("Exception in data cleaning")
# data_Cleaning(df)

def calc_distance(df):    
    try:
        logging.info("Distance calculation started")
        df = df.dropna()
        # Set the earth's radius (in kilometers)
        R = 6371
        index = []
        # Convert degrees to radians
        def deg_to_rad(degrees):
            return degrees * (np.pi/180)

        # Function to calculate the distance between two points using the haversine formula
        def distcalculate(lat1, lon1, lat2, lon2):
            d_lat = deg_to_rad(lat2-lat1)
            d_lon = deg_to_rad(lon2-lon1)
            a = np.sin(d_lat/2)**2 + np.cos(deg_to_rad(lat1)) * np.cos(deg_to_rad(lat2)) * np.sin(d_lon/2)**2
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
            return R * c
        
        # Calculate the distance between each pair of points
        # data1['distance'] = np.nan

        for i in range(len(df)):
            if i in df.index:
                df.loc[i, 'distance'] = distcalculate(df.loc[i, 'Restaurant_latitude'], 
                                                df.loc[i, 'Restaurant_longitude'], 
                                                df.loc[i, 'Delivery_location_latitude'], 
                                                df.loc[i, 'Delivery_location_longitude'])
            else:
                index.append(i)
        logging.info('distance calculation ended')
        return df
    except Exception as e:
        logging.info("Exception raised in distance calculation")


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_model(X_train,y_train,X_test,y_test,models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            # Train model
            model.fit(X_train,y_train)

            

            # Predict Testing data
            y_test_pred =model.predict(X_test)

            # Get R2 scores for train and test data
            #train_model_score = r2_score(ytrain,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] =  test_model_score

        return report

    except Exception as e:
        logging.info('Exception occured during model training')
        raise CustomException(e,sys)
    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info('Exception Occured in load_object function utils')
        raise CustomException(e,sys)
import json
# import pymongo as pym
import pandas as pd
import os
from pymongo.mongo_client import MongoClient

dbName = input("Enter the Database name: ")
dbPassword = input("Enter the Database password: ")

# Create a new client and connect to the server
client = MongoClient("mongodb+srv://"+dbName+":"+dbPassword+"@cluster0.3bxeryk.mongodb.net/?retryWrites=true&w=majority")


df = pd.read_csv("https://raw.githubusercontent.com/AKISHPOTHURI/DataScience/main/Dataset/online_order.csv")
data_dict = df.to_dict("records")

db = client["delivery"]#database created
deliveryData = db["delivery"]#collection created

deliveryData.insert_many(data_dict)
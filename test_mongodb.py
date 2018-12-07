from pymongo import MongoClient
from random import randint
from datetime import datetime

#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient('mongodb://192.168.1.144:27017/')
db=client.test_db
#print(client)
#print(db)
result=db.users.insert_one({'a':'a'})

import pymongo
import numpy as np
from struct import *

_author_ = 'Boyi Li'

class Database:

    def __init__(self, uri):
        self.uri = uri            # "mongodb://192.168.1.144:27017"
        self.client = pymongo.MongoClient(uri)
        self.database = self.client['test_db']
        self.collection = self.database['users']

    def read_records(self, N=39):
        count = self.collection.count() - N
        wizards = self.collection.find().skip(count) if count >= 0 else self.collection.find().skip(0)
        return wizards




# def preprocess(wizards):
#     if wizards["wave_id"]
#     data_lst = []
#     for data in wizards:
#         data_lst += data['data']
#     data_arr = np.array(data_lst)
#     return data_arr.T







import sys

# database = Database("mongodb://192.168.1.144:27017")
# # #
# wizards = database.read_records(11)
# packet = []
# for data in wizards:
#     for i in range(0, len(data['data']), 4):
#         packet.append(unpack('f', data['data'][i:i+4])[0])
# packet_arr = np.array(packet).reshape(-1, 8)
# print(packet_arr.max())
# print(packet_arr.shape)
    # print(data['data'][1])

# print(packet_arr.T)

    # tes = bson.BSON.encode(data['data'])
    # print(tes)
# print(wizards)
# print(preprocess(wizards).shape)




# for wizard in wizards:
#     print(wizard)
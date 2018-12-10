import pymongo

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




database = Database("mongodb://192.168.1.144:27017")

wizards = database.read_records(39)
for wizard in wizards:
    print(wizard)
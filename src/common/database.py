import pymongo
import os


class Database(object):
    URI = os.getenv('MONGO_DB')
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['covid19']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection):
        return Database.DATABASE[collection].find().sort("_id", -1)


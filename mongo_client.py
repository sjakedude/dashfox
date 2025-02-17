from pymongo import MongoClient
from bson import ObjectId


class ConeMongoClient:
    def __init__(self):
        self.ip = "192.168.0.100"
        self.uri = f"mongodb://admin:secret@{self.ip}:27017/admin"
        self.client = MongoClient(self.uri)
        self.db = self.client["xbox_360"]
        self.collection = None

    def set_collection(self, collection_name):
        self.collection = self.db[collection_name]

    def insert_ftp_dump(self, ftp_dump):
        self.collection = self.db["ftp_dump"]
        self.collection.insert_one(ftp_dump)

    def get_lastest_ftp_dump(self):
        self.collection = self.db["ftp_dump"]
        latest_ftp_dump_object = self.collection.find_one(sort=[("_id", -1)])
        return latest_ftp_dump_object

    def get_all_ftp_dump(self):
        self.collection = self.db["ftp_dump"]
        records = []
        for ftp_dump_object in self.collection.find():
            records.append(ftp_dump_object)
        return records

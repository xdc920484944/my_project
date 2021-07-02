import pymongo
from pymongo.collection import Collection

from config import DEBUG, MONGO_DB


class MonGo:
    def __init__(self):
        self.db = self.mongo_conn()

    @staticmethod
    def mongo_conn():
        if DEBUG:
            conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
        else:
            CONN_ADDR1 = 'uf684000330843141.mongodb.rds.aliyuncs.com:3717'
            CONN_ADDR2 = 'dds-uf684000330843142.mongodb.rds.aliyuncs.com:3717'
            REPLICAT_SET = 'mgset-53057590'
            username = 'root'
            password = 'sdfjk3_KDLkj3209_dfls'
            # 获取mongoclient
            conn = pymongo.MongoClient([CONN_ADDR1, CONN_ADDR2], replicaSet=REPLICAT_SET)
            # 授权。 这里的user基于admin数据库授权。
            conn.admin.authenticate(username, password)
        db = conn[MONGO_DB]
        return db

    def insert_data(self, collection, data):
        collection = Collection(self.db, collection)
        if type(data) is list:
            collection.insert_many(data)
        else:
            collection.insert_one(data)

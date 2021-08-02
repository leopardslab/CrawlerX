import pymongo
import logging
import json
from bson import json_util

from crawlerx_server.settings import MONGODB_DATABASE, MONGODB_HOSTNAME, MONGODB_PORT


class MongoConnection:
    mongo_uri = 'mongodb://' + MONGODB_HOSTNAME + ':' + MONGODB_PORT
    mongo_db = MONGODB_DATABASE

    def __init__(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_connection(self):
        # clean up when db is closed
        self.client.close()

    def insert_item(self, data_item, collection_name):
        # how to handle each post
        self.db[collection_name].insert(data_item, True)
        logging.info("Post inserted to MongoDB")

    def upsert_item(self, query, data_item, collection_name):
        # how to handle each post
        self.db[collection_name].update(query, data_item, True)
        logging.info("Post added to MongoDB")

    def update_item(self, query, data_item, collection_name):
        # how to handle each post
        self.db[collection_name].update_one(query, data_item, True)
        logging.info("Post added to MongoDB")

    def get_items(self, collection_name, query):
        # retrieve data from database
        cursor = self.db[collection_name].find(query)
        json_docs = []
        for doc in cursor:
            json_doc = json.dumps(doc, default=json_util.default)
            json_docs.append(json.loads(json_doc))
        return json_docs

    def delete_items(self, collection_name, query):
        cursor = self.db[collection_name].delete_many(query)
        return int(cursor.deleted_count)



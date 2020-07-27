import pymongo
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('logs')


class ScrapyAppPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            logger.debug("Connection has been established to the MongoDB client")
        except Exception as e:
            logger.debug("Error while connecting to the MongoDB client" + str(e))

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        query = {'unique_id': item['unique_id'], 'user_id': item['user_id'],
                 'task_id': item['task_id'], 'project_id': item['project_id']}

        # name of the all crawled data stored collection
        crawled_data_collection_name = 'crawled_data'
        # name of the all job details stored collection
        job_collection_name = 'jobs'

        try:
            self.db[crawled_data_collection_name].update(query, dict(item), True)
            logger.debug("Crawled data has been added to the MongoDB database successfully")

            self.db[job_collection_name].update_one(query, {'$set': {"status": "COMPLETED"}})
            logger.debug("Job data field has been successfully updated for the scheduled job")
        except Exception as e:
            self.db[job_collection_name].update_one(query, {'$set': {"status": "FAILED"}})
            logger.debug("Job data field has been updated for the scheduled job" + str(e))

        return item

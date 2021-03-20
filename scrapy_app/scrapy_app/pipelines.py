import pymongo
import logging
import json
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('logs')


class ScrapyAppPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.es = Elasticsearch(HOST="http://elasticsearch", PORT=9200)

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
        self.es.close()

    def process_item(self, item, spider):
        query = {'unique_id': item['unique_id'], 'user_id': item['user_id'],
                 'task_id': item['task_id'], 'job_name': item['job_name'], 'project_name': item['project_name']}

        # name of the all crawled data stored collection
        crawled_data_collection_name = 'crawled_data'
        # name of the all job details stored collection
        job_collection_name = 'jobs'

        try:
            self.db[crawled_data_collection_name].update(query, dict(item), True)
            logger.debug("Crawled data has been added to the MongoDB database successfully")

            self.db[job_collection_name].update_one(query, {'$set': {"status": "COMPLETED"}})
            logger.debug("Job data field has been successfully updated for the scheduled job")

            # add data into the elastic search
            try:
                element_id = item['unique_id'].lower() + '-' + item['task_id'].lower()
                index = item['user_id'].lower()
                index_exists = self.es.indices.exists(index=index)

                if not index_exists:
                    self.es.indices.create(index=index)
                item_body = json.dumps(item, default=lambda o: o.__dict__, sort_keys=True, indent=4)
                self.es.index(index=index, id=element_id, body=item_body)
                print("Crawled data successfully indexed in the ElasticSearch")
                logger.info("Crawled data successfully indexed in the ElasticSearch")
            except Exception as e:
                logger.debug("Error while inserting data into the ElasticSearch" + str(e))
        except Exception as e:
            self.db[job_collection_name].update_one(query, {'$set': {"status": "FAILED"}})
            logger.debug("Job data field has been updated for the scheduled job" + str(e))

        return item


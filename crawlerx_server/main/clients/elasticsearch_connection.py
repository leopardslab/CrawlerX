import logging
from elasticsearch import Elasticsearch


class ELKConnection:
    elk_uri = 'http://elasticsearch'
    elk_port = 9200

    def __init__(self):
        self.es = Elasticsearch(HOST=self.elk_uri, PORT=self.elk_port)
        logging.info("Connection between ElasticSearch has been established")

    def close_connection(self):
        # clean up when db is closed
        self.es.close()

    def get_data_from_query(self, req_index, body):
        try:
            if self.es.indices.exists(index=req_index):
                res = self.es.search(index=req_index, body=body)
                return res
        except Exception as e:
            logging.error("Error while getting data from the ElasticSearch" + str(e))



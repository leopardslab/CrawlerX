import logging
from elasticsearch import Elasticsearch

from crawlerx_server.settings import ELASTIC_SEARCH_USERNAME, ELASTIC_SEARCH_PASSWORD, ELASTIC_SEARCH_HOSTNAME, \
    ELASTIC_SEARCH_PORT


class ELKConnection:
    elk_uri = 'http://' + ELASTIC_SEARCH_USERNAME + ':' + ELASTIC_SEARCH_PASSWORD + '@' + ELASTIC_SEARCH_HOSTNAME \
              + ':' + ELASTIC_SEARCH_PORT

    def __init__(self):
        self.es = Elasticsearch(hosts=self.elk_uri)
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



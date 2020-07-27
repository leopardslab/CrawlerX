from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from scrapyd_api import ScrapydAPI
from urllib.parse import urlparse
import json
import logging

# connect scrapyd service
from mongo_connection import MongoConnection

scrapyd = ScrapydAPI('http://localhost:6800')

# connect to the rabbitMQ broker
rabbit_url = "amqp://guest:guest@localhost:5672/"

# Creating an object for logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def schedule_crawl_job(body):
    # sample format of the consumed body
    # {
    #     "unique_id": "unique_id",
    #     "project_id": "project_id",
    #     "url": "url",
    #     "user_id": "user_id",
    #     "task_id": null,
    #     "status": "PENDING",
    # }

    try:
        logger.info("Crawl job data has been consumed")
        body = body.replace("'", "\"")
        json_body = json.loads(body)
        unique_id = json_body["unique_id"]
        job_url = json_body["url"]
        project_id = json_body["project_id"]
        user_id = json_body["user_id"]
        status = json_body["status"]
        crawler_name = json_body["crawler_name"]

        if not unique_id or not job_url or not project_id or not user_id or not status or not crawler_name:
            raise Exception('Required parameters are missing in the consumed message')

        job_domain = urlparse(job_url).netloc
        try:
            settings = {
                'unique_id': unique_id,
                'user_id': user_id,
                'project_id': project_id,
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }

            # to list available spiders in the project
            # print(scrapyd.list_spiders("crawlerx_project"))

            # Schedule a crawl job with project and a specific spider
            task_id = \
                scrapyd.schedule("crawlerx_project", crawler_name, settings=settings, url=job_url, domain=job_domain)

            # update relevant MongoDC entry in jobs collection with task_id and status
            update_data = u'{ "unique_id": "' + unique_id + '", "url": "' + job_url + '", "project_id": "' \
                          + project_id + '", "user_id": "' + user_id + '", "crawler_name": "' + crawler_name \
                          + '", "task_id": "' + task_id + '", "status": "RUNNING" }'

            data_item = json.loads(update_data)
            query = {'user_id': user_id, 'url': job_url, 'project_id': project_id, 'crawler_name': crawler_name}
            mongo_connection = MongoConnection()
            mongo_connection.upsert_item(query, data_item, "jobs")
            mongo_connection.close_connection()

            # task id of the crawl job
            logger.info("Crawling job has been started with ID - " + task_id)
        except Exception as e:
            logger.exception("Error while scheduling the crawl job with default project, " + str(e))
    except Exception as e:
        logger.exception("Consumed crawl job is not in required JSON format, " + str(e))


class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues, callbacks=[self.on_message])]

    def on_message(self, body, message):
        schedule_crawl_job(format(body))
        message.ack()


exchange = Exchange("example-exchange", type="direct")
queues = [Queue("example-queue", exchange, routing_key="BOB")]

with Connection(rabbit_url, heartbeat=10) as conn:
    try:
        logger.info("RabbitMQ consumer has been started")
        worker = Worker(conn, queues)
        worker.run()
    except KeyboardInterrupt:
        logger.info("Goodbye")
        exit(0)
    except:
        raise

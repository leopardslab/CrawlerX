from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from scrapyd_api import ScrapydAPI
from urllib.parse import urlparse
import json
import logging

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

# connect to the rabbitMQ broker
rabbit_url = "amqp://guest:guest@localhost:5672/"


def schedule_crawl_job(body):
    # sample format of the consumed body
    # {
    #     "unique_id": "dsadasdasdasdasdadadasasda",
    #     "project_name": "default",
    #     "url": "www.wso2.com"
    # }

    global job_id
    try:
        logging.info("Crawl job data has been consumed")
        json_body = json.loads(body)
        job_id = json_body["unique_id"]
        job_url = json_body["url"]
        job_domain = urlparse(job_url).netloc
    except:
        logging.exception("Consumed crawl job is not in required JSON format")

    try:
        settings = {
            'unique_id': job_id,
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # to list available spiders in the project
        # print(scrapyd.list_spiders(job_project))

        # Schedule a crawl job with project and a specific spider
        # task = scrapyd.schedule(job_project, 'crawlerx', settings=settings, url=job_url, domain=job_domain)

        # task id of the crawl job
        # print(task)
    except:
        logging.exception("Error while scheduling the crawl job with default project")


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
        print("Connection started")
        worker = Worker(conn, queues)
        worker.run()
    except KeyboardInterrupt:
        print("Goodbye")
        exit(0)
    except:
        raise

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from scrapyd_api import ScrapydAPI
from urllib.parse import urlparse
import json
import logging
import requests
from requests.exceptions import ConnectionError
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from mongo_connection import MongoConnection

# connect scrapyd service
scrapyd = ScrapydAPI('http://scrapyd:6800')

# connect to the rabbitMQ broker
rabbit_url = "amqp://guest:guest@rabbitmq:5672/"

# Creating an object for logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_url_gives_response(url):
    url_available = True
    try:
        response = requests.get(url)
        if (response.status_code % 100) == 4:
            url_available = False
    except ConnectionError:
        url_available = False

    return url_available


def schedule_job_on_datetime(body):
    run_crawl_job(body)


def schedule_crawl_job(body):
    # sample format of the consumed body
    # {
    #     "unique_id": "unique_id",
    #     "project_name": "project_name",
    #     "job_name": "job_name",
    #     "url": "url",
    #     "user_id": "user_id",
    #     "task_id": null,
    #     "schedule_date": "schedule_date",
    #     "schedule_time": "schedule_time"
    # }
    logger.info("Crawl job data has been consumed")
    try:
        body = body.replace("'", "\"")
        json_body = json.loads(body)
        schedule_date = json_body["schedule_date"]
        schedule_time = json_body["schedule_time"]

        if schedule_date or schedule_time:
            if not schedule_date:
                schedule_date = date.today().strftime('%Y-%m-%d')

            if not schedule_time:
                schedule_time = "00:00:00"

            try:
                start_date_time = schedule_date + " " + schedule_time
                expiration_date = datetime.strptime(start_date_time, "%Y-%m-%d %H:%M:%S")
                now_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                now_date = datetime.strptime(now_time_string, "%Y-%m-%d %H:%M:%S")

                if expiration_date < now_date:
                    raise Exception(start_date_time + '  was missed by python scheduler')

                scheduler = BackgroundScheduler(daemon=True)
                scheduler.add_job(schedule_job_on_datetime, trigger='date', next_run_time=start_date_time, args=[body])
                scheduler.start()
                logger.info("Crawl job scheduled to the Date: " + schedule_date + " and Time: " + schedule_time)
            except Exception as e:
                json_body = json.loads(body)
                unique_id = json_body["unique_id"]
                job_url = json_body["url"]
                project_name = json_body["project_name"]
                job_name = json_body["job_name"]
                user_id = json_body["user_id"]
                crawler_name = json_body["crawler_name"]

                # update relevant MongoDC entry in jobs collection with task_id and status
                update_data = u'{ "unique_id": "' + unique_id + '", "url": "' + job_url + '", "project_name": "' \
                              + project_name + '", "job_name": "' + job_name + '", "user_id": "' + user_id \
                              + '", "crawler_name": "' + crawler_name \
                              + '", "task_id": "Not Generated", "status": "FAILED" }'

                data_item = json.loads(update_data)
                query = {'user_id': user_id, 'url': job_url, 'project_name': project_name, 'job_name': job_name,
                         'crawler_name': crawler_name}
                mongo_connection = MongoConnection()
                mongo_connection.upsert_item(query, data_item, "jobs")
                mongo_connection.close_connection()

                logger.exception("Current can not schedule with invalid date or time format. "
                                 "Hence, job execution failed. " + str(e))
        else:
            run_crawl_job(body)
    except Exception as e:
        logger.exception("Consumed crawl job is not in required JSON format, " + str(e))


def run_crawl_job(body):
    try:
        json_body = json.loads(body)
        unique_id = json_body["unique_id"]
        job_url = json_body["url"]
        project_name = json_body["project_name"]
        job_name = json_body["job_name"]
        user_id = json_body["user_id"]
        status = json_body["status"]
        crawler_name = json_body["crawler_name"]

        if not unique_id or not job_url or not project_name or not user_id or not status \
                or not crawler_name or not job_name:
            raise Exception('Required parameters are missing in the consumed message')

        if check_url_gives_response(job_url):
            job_domain = urlparse(job_url).netloc
            try:
                settings = {
                    'unique_id': unique_id,
                    'user_id': user_id,
                    'job_name': job_name,
                    'project_name': project_name,
                    'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
                }

                # to list available spiders in the project
                # print(scrapyd.list_spiders("crawlerx_project"))

                # Schedule a crawl job with project and a specific spider
                task_id = \
                    scrapyd.schedule("crawlerx_project", crawler_name, settings=settings, url=job_url,
                                     domain=job_domain)

                # update relevant MongoDC entry in jobs collection with task_id and status
                update_data = u'{ "unique_id": "' + unique_id + '", "url": "' + job_url + '", "project_name": "' \
                              + project_name + '", "job_name": "' + job_name + '", "user_id": "' + user_id \
                              + '", "crawler_name": "' + crawler_name \
                              + '", "task_id": "' + task_id + '", "status": "RUNNING" }'

                data_item = json.loads(update_data)
                query = {'user_id': user_id, 'url': job_url, 'project_name': project_name, 'job_name': job_name,
                         'crawler_name': crawler_name}
                mongo_connection = MongoConnection()
                mongo_connection.upsert_item(query, data_item, "jobs")
                mongo_connection.close_connection()

                # task id of the crawl job
                logger.info("Crawling job has been started with ID - " + task_id)
            except Exception as e:
                logger.exception("Error while scheduling the crawl job with default project, " + str(e))
        else:
            # update relevant MongoDC entry in jobs collection with task_id and status
            update_data = u'{ "unique_id": "' + unique_id + '", "url": "' + job_url + '", "project_name": "' \
                          + project_name + '", "job_name": "' + job_name + '", "user_id": "' + user_id \
                          + '", "crawler_name": "' + crawler_name \
                          + '", "task_id": "Not Generated", "status": "FAILED" }'

            data_item = json.loads(update_data)
            query = {'user_id': user_id, 'url': job_url, 'project_name': project_name, 'job_name': job_name,
                     'crawler_name': crawler_name}
            mongo_connection = MongoConnection()
            mongo_connection.upsert_item(query, data_item, "jobs")
            mongo_connection.close_connection()

            logger.exception("Current job URL does not seems available. Hence, job execution failed.")
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

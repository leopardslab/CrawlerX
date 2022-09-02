from celery import shared_task
from scrapyd_api import ScrapydAPI
from urllib.parse import urlparse
import logging
import json
import requests
import time

# connect scrapy daemon service
from crawlerx_server.settings import SCRAPY_API_HOSTNAME, SCRAPY_API_PORT
from main.clients.mongo_connection import MongoConnection

scrapy_daemon = ScrapydAPI('http://' + SCRAPY_API_HOSTNAME + ':' + SCRAPY_API_PORT)

# Creating an object for logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def handle_fault_execution(request, schedule_time, exception):
    unique_id = request["unique_id"]
    job_url = request["url"]
    project_name = request["project_name"]
    job_name = request["job_name"]
    user_id = request["user_id"]
    crawler_name = request["crawler_name"]
    schedule_category = request["schedule_category"]

    # update relevant MongoDC entry in jobs collection with task_id and status
    update_data = u'{ "unique_id": "' + unique_id + '", "url": "' + job_url + '", "project_name": "' \
                  + project_name + '", "job_name": "' + job_name + '", "user_id": "' + user_id \
                  + '", "crawler_name": "' + crawler_name \
                  + '", "task_id": "Not Generated", "status": "FAILED" }'

    data_item = json.loads(update_data)
    data_item['schedule_category'] = schedule_category
    data_item['schedule_time'] = schedule_time

    mongo_connection = MongoConnection()
    if schedule_category == "Instant":
        # update relevant MongoDC entry in jobs collection with task_id and status
        query = {'user_id': user_id, 'url': job_url, 'project_name': project_name, 'job_name': job_name,
                 'crawler_name': crawler_name}
        mongo_connection.upsert_item(query, data_item, "jobs")
    else:
        # store job records in MongoDB database
        mongo_connection.insert_item(data_item, "jobs")
    logger.exception("Current can not schedule with invalid date or time format. "
                     "Hence, job execution failed. " + str(exception))


def check_url_gives_response(url):
    url_available = True
    try:
        response = requests.get(url)
        if (response.status_code % 100) == 4:
            url_available = False
    except ConnectionError:
        url_available = False

    return url_available


# sample format of the consumed body
    # {
    #     "unique_id": "unique_id",
    #     "project_name": "project_name",
    #     "job_name": "job_name",
    #     "url": "url",
    #     "user_id": "user_id",
    #     "task_id": null,
    # }

@shared_task(bind=True)
def schedule_cron_job(self, **kwargs):
    json_body = ""
    schedule_time = str(time.time())
    try:
        json_body = kwargs
        if "kwargs" in json_body:
            json_body = json.loads(json_body['kwargs'])
        unique_id = json_body['unique_id']
        job_url = json_body["url"]
        project_name = json_body["project_name"]
        job_name = json_body["job_name"]
        user_id = json_body["user_id"]
        status = json_body["status"]
        crawler_name = json_body["crawler_name"]
        schedule_category = json_body["schedule_category"]

        if not unique_id or not job_url or not project_name or not user_id or not status \
                or not crawler_name or not job_name:
            raise Exception('Required parameters are missing in the consumed message')

        is_valid_url = True
        if crawler_name != "tor_onion":
            is_valid_url = check_url_gives_response(job_url)
            job_domain = urlparse(job_url).netloc
        else:
            job_domain = job_url

        if is_valid_url:
            try:
                settings = {
                    'unique_id': unique_id,
                    'user_id': user_id,
                    'job_name': job_name,
                    'project_name': project_name,
                    'schedule_time': schedule_time,
                    'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
                }

                # to list available spiders in the project
                # print(scrapyd.list_spiders("crawlerx_project"))

                # Schedule a crawl job with project and a specific spider
                task_id = scrapy_daemon.schedule("crawlerx_project", crawler_name, settings=settings,
                                           url=job_url, domain=job_domain)

                mongo_connection = MongoConnection()

                job_data = u'{ "unique_id": "' + unique_id + '", "url": "' + job_url + '", "project_name": "' \
                           + project_name + '", "job_name": "' + job_name + '", "user_id": "' + user_id \
                           + '", "crawler_name": "' + crawler_name \
                           + '", "task_id": "' + task_id + '", "status": "RUNNING" }'
                data_item = json.loads(job_data)
                data_item['schedule_category'] = schedule_category
                data_item['schedule_time'] = schedule_time

                if schedule_category == "Instant":
                    # update relevant MongoDC entry in jobs collection with task_id and status
                    query = {'user_id': user_id, 'url': job_url, 'project_name': project_name, 'job_name': job_name,
                             'crawler_name': crawler_name}
                    mongo_connection.upsert_item(query, data_item, "jobs")
                else:
                    # store job records in MongoDB database
                    mongo_connection.insert_item(data_item, "jobs")

                # task id of the crawl job
                logger.info("Crawling job has been started with ID - " + task_id)
            except Exception as e:
                handle_fault_execution(json_body, schedule_time, e)
        else:
            handle_fault_execution(json_body, schedule_time,
                                   Exception("Current job URL does not seems available. Hence, job execution failed."))
    except Exception as e:
        handle_fault_execution(json_body, schedule_time, e)

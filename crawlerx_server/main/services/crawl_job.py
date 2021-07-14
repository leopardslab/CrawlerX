from json import JSONDecodeError
from uuid import uuid4
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.clients.mongo_connection import MongoConnection
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
import json
import time
from main.tasks import schedule_cron_job

SCHEDULE_TASK_TYPE = "SCHEDULE_TASK"
INTERVAL_TASK_TYPE = "INTERVAL_TASK"
HOT_TASK_TYPE = "HOT_TASK"
DAYS = "DAYS"
HOURS = "HOURS"
MINUTES = "MINUTES"
SECONDS = "SECONDS"


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True


def schedule_job_with_interval(request):
    try:
        user_id = request['user_id']
        schedule_data = request['schedule_data']
        occurrence = schedule_data['occurrence']
        granularity = schedule_data['granularity']

        if not occurrence:
            return JsonResponse({'status': "400 BAD",
                                 'Error': 'Missing occurrence key in the request payload'})

        if not granularity:
            return JsonResponse({'status': "400 BAD",
                                 'Error': 'Missing granularity key in the request payload'})

        if granularity == DAYS:
            granularity_value = IntervalSchedule.DAYS
        elif granularity == HOURS:
            granularity_value = IntervalSchedule.HOURS
        elif granularity == MINUTES:
            granularity_value = IntervalSchedule.MINUTES
        elif granularity == SECONDS:
            granularity_value = IntervalSchedule.SECONDS
        else:
            return JsonResponse({'status': "400 BAD", 'Error': 'Granularity value is not valid'})

        del request['schedule_data']  # remove schedule meta data
        schedule, created = IntervalSchedule.objects.get_or_create(every=occurrence, period=granularity_value)
        interval_task = PeriodicTask.objects.create(interval=schedule,
                                                    name=user_id + "-interval-task-" + str(time.time()),
                                                    task='main.tasks.schedule_cron_job', kwargs=json.dumps(request))
        return interval_task
    except Exception as e:
        return JsonResponse({'status': "400 BAD",
                             'Error': 'Required fields occurrence and granularity values not found or empty, '
                                      + str(e)})


def schedule_job_with_cron_tab(request):
    try:
        user_id = request['user_id']
        schedule_data = request['schedule_data']
        minute = schedule_data['schedule_minute']
        hour = schedule_data['schedule_hour']
        day_of_week = schedule_data['day_of_week']
        day_of_month = schedule_data['day_of_month']
        month_of_year = schedule_data['month_of_year']

        if not minute:
            return JsonResponse({'status': "400 BAD",
                                 'Error': 'Missing minute key in the request payload'})

        if not hour:
            return JsonResponse({'status': "400 BAD",
                                 'Error': 'Missing hour key in the request payload'})

        if not day_of_week:
            return JsonResponse({'status': "400 BAD",
                                 'Error': 'Missing day_of_week key in the request payload'})

        if not day_of_month:
            return JsonResponse({'status': "400 BAD",
                                 'Error': 'Missing day_of_month key in the request payload'})

        if not month_of_year:
            return JsonResponse({'status': "400 BAD",
                                 'Error': 'Missing month_of_year key in the request payload'})

        del request['schedule_data']  # remove schedule meta data
        schedule, created = CrontabSchedule.objects.get_or_create(minute=minute, hour=hour,
                                                                  day_of_week=day_of_week,
                                                                  day_of_month=day_of_month,
                                                                  month_of_year=month_of_year)
        scheduled_task = PeriodicTask.objects.create(crontab=schedule,
                                                     name=user_id + "-schedule-task-" + str(time.time()),
                                                     task='main.tasks.schedule_cron_job', kwargs=json.dumps(request))
        return scheduled_task
    except Exception as e:
        return JsonResponse({'status': "400 BAD",
                             'Error': 'Required fields schedule_minute, schedule_hour, day_of_week, day_of_month '
                                      'and  month_of_year values not found or empty, ' + str(e)})


@csrf_exempt
@require_http_methods(['POST'])  # only post
def crawl_new_job(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        # take urls comes from client.
        try:
            json_data = json.loads(request.body)
            url_data = json_data['urls']
            job_name = json_data['job_name']
            project_name = json_data['project_name']
            user_id = json_data['user_id']
            crawler_name = json_data['crawler_name']
            schedule_type = json_data['schedule_type']
            schedule_data = json_data['schedule_data']
        except (JSONDecodeError, KeyError) as e:
            return JsonResponse({'Error': 'Missing fields in the request payload or empty, ' + str(e)})

        if not user_id:
            return JsonResponse({'Error': 'Missing user id key in the request payload'})

        if not job_name:
            return JsonResponse({'Error': 'Missing job name key in the request payload'})

        if not url_data:
            return JsonResponse({'Error': 'Missing urls key in the request payload'})

        if not project_name:
            return JsonResponse({'Error': 'Missing project_name key in the request payload'})

        if not crawler_name:
            return JsonResponse({'Error': 'Missing crawler_name key in the request payload'})

        if not schedule_type:
            return JsonResponse({'Error': 'Missing schedule_type key in the request payload'})

        if (schedule_type != SCHEDULE_TASK_TYPE) \
                and (schedule_type != INTERVAL_TASK_TYPE) and (schedule_type != HOT_TASK_TYPE):
            return JsonResponse({'Error': 'Requested crawler_type:' + schedule_type + ' is not a valid type'})

        publish_url_ids = []
        for url in url_data:
            if not is_valid_url(url):
                return JsonResponse({'error': url + ' URL is invalid'})

            unique_id = str(uuid4())  # create a unique ID.
            publish_data = u'{ "unique_id": "' + unique_id + '", "job_name": "' + job_name \
                           + '", "url": "' + url + '", "project_name": "' \
                           + project_name + '", "user_id": "' + user_id + '", "crawler_name": "' + crawler_name \
                           + '", "task_id":"", "status": "PENDING" }'

            publish_data = json.loads(publish_data)
            try:
                # schedule data with celery task scheduler
                if schedule_type == SCHEDULE_TASK_TYPE:
                    publish_data['schedule_data'] = schedule_data
                    celery_task = schedule_job_with_cron_tab(publish_data)
                elif schedule_type == INTERVAL_TASK_TYPE:
                    publish_data['schedule_data'] = schedule_data
                    celery_task = schedule_job_with_interval(publish_data)
                else:
                    celery_task = schedule_cron_job.delay(kwargs=json.dumps(publish_data))

                if isinstance(celery_task, JsonResponse):
                    return celery_task

                publish_url_ids.append(unique_id)
                publish_data['celery_task_name'] = celery_task.name
                try:
                    # store job records in MongoDB database
                    query = {'user_id': user_id, 'job_name': job_name, 'url': url,
                             'project_name': project_name, 'crawler_name': crawler_name}
                    mongo_connection = MongoConnection()
                    mongo_connection.upsert_item(query, publish_data, "jobs")
                except Exception as e:
                    return JsonResponse({'Error': 'Error while connecting to the MongoDB database, ' + str(e)})
            except Exception as e:
                return JsonResponse({'status': "400 BAD",
                                     'Exception': 'Error occurred while scheduling the data with the Celery executor, '
                                                  + str(e)})

        return JsonResponse({'status': "SUCCESS", 'job_ids': publish_url_ids})


@csrf_exempt
@require_http_methods(['POST'])  # only post
def get_crawl_data(request):
    # take urls comes from client.
    try:
        json_data = json.loads(request.body)
        user_id = json_data['user_id']
        task_id = json_data['task_id']
    except JSONDecodeError as e:
        return JsonResponse({'Error': 'Missing URLs in the request payload or empty, ' + str(e)})

    if not user_id:
        return JsonResponse({'Error': 'Missing user id key in the request payload'})

    if not task_id:
        return JsonResponse({'Error': 'Missing task id key in the request payload'})

    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("crawled_data", {'user_id': user_id, 'task_id': task_id})
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting project details from the database, ' + str(e)})

    return JsonResponse({'status': "SUCCESS", 'data': json_data})

@csrf_exempt
@require_http_methods(['POST'])  # only post
def get_job_data(request):
    # take urls comes from client.
    try:
        json_data = json.loads(request.body)
        user_id = json_data['user_id']
        unique_id = json_data['unique_id']
    except JSONDecodeError as e:
        return JsonResponse({'Error': 'Missing URLs in the request payload or empty, ' + str(e)})

    if not user_id:
        return JsonResponse({'Error': 'Missing user id key in the request payload'})

    if not unique_id:
        return JsonResponse({'Error': 'Missing unique id key in the request payload'})

    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("jobs", {'user_id': user_id, 'unique_id': unique_id})
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting project details from the database, ' + str(e)})

    return JsonResponse({'status': "SUCCESS", 'data': json_data})


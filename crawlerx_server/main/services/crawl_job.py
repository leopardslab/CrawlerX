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
INSTANT = "Instant"
INTERVAL = "Interval"
CRON = "Cron"


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
            return JsonResponse({'Status': "400 BAD",
                                 'Error': 'Missing occurrence key in the request payload'}, status=400)

        if not granularity:
            return JsonResponse({'Status': "400 BAD",
                                 'Error': 'Missing granularity key in the request payload'}, status=400)

        if granularity == DAYS:
            granularity_value = IntervalSchedule.DAYS
        elif granularity == HOURS:
            granularity_value = IntervalSchedule.HOURS
        elif granularity == MINUTES:
            granularity_value = IntervalSchedule.MINUTES
        elif granularity == SECONDS:
            granularity_value = IntervalSchedule.SECONDS
        else:
            return JsonResponse({'Status': "400 BAD", 'Error': 'Granularity value is not valid'}, status=400)

        del request['schedule_data']  # remove schedule meta data
        schedule, created = IntervalSchedule.objects.get_or_create(every=occurrence, period=granularity_value)
        interval_task = PeriodicTask.objects.create(interval=schedule,
                                                    name=user_id + "-interval-task-" + str(time.time()),
                                                    task='main.tasks.schedule_cron_job', kwargs=json.dumps(request))
        return interval_task
    except Exception as e:
        return JsonResponse({'Status': "400 BAD",
                             'Error': 'Required fields occurrence and granularity values not found or empty, '
                                      + str(e)}, status=400)


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
            return JsonResponse({'Status': "400 BAD",
                                 'Error': 'Missing minute key in the request payload'}, status=400)

        if not hour:
            return JsonResponse({'Status': "400 BAD",
                                 'Error': 'Missing hour key in the request payload'}, status=400)

        if not day_of_week:
            return JsonResponse({'Status': "400 BAD",
                                 'Error': 'Missing day_of_week key in the request payload'}, status=400)

        if not day_of_month:
            return JsonResponse({'Status': "400 BAD",
                                 'Error': 'Missing day_of_month key in the request payload'}, status=400)

        if not month_of_year:
            return JsonResponse({'Status': "400 BAD",
                                 'Error': 'Missing month_of_year key in the request payload'}, status=400)

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
        return JsonResponse({'Status': "400 BAD",
                             'Error': 'Required fields schedule_minute, schedule_hour, day_of_week, day_of_month '
                                      'and  month_of_year values not found or empty, ' + str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])  # only post
def disable_schedule_job(request):

    if request.method == 'POST':
        task_name = ""
        try:
            json_data = json.loads(request.body)
            task_name = json_data['celery_task_name']
            is_enabled = json_data['is_enabled']
            task = PeriodicTask.objects.get(name=task_name)
            if not task:
                return JsonResponse({'Error': 'Scheduled task_name: ' + task_name + ' is invalid or does not exist'}
                                    , status=400)
            if type(is_enabled) != bool:
                return JsonResponse({'Error': 'Scheduled is_enabled: ' + is_enabled + ' is invalid parameter'}
                                    , status=400)
            task.enabled = is_enabled
            task.save()
            mongo_connection = MongoConnection()
            if is_enabled:
                mongo_connection.update_item({"celery_task_name": task_name, "status": "DISABLED"},
                                             {'$set': {"status": "RUNNING"}}, "jobs")
                value = "enabled"
            else:
                mongo_connection.update_item({"celery_task_name": task_name, "status": "RUNNING"},
                                             {'$set': {"status": "DISABLED"}}, "jobs")
                value = "disabled"
            return JsonResponse({'Status': "SUCCESS",
                                 'Message': 'Successfully ' + value + ' the scheduled task_name: ' + task_name})
        except Exception as e:
            return JsonResponse({'status': "400 BAD",
                                 'Error': 'Error occurred while disabling the scheduled task task_name: '
                                          + task_name + ". " + str(e)}, status=400)


def delete_schedule_job(task_name):
    try:
        task = PeriodicTask.objects.get(name=task_name)
        if not task:
            return JsonResponse({'Error': 'Scheduled task_name: ' + task_name + ' is invalid or does not exist'},
                                status=400)

        task.delete()
        return True
    except Exception as e:
        return JsonResponse({'Status': "400 BAD",
                             'Error': 'Error occurred while deleting the scheduled task_name: '
                                      + task_name + ". " + str(e)}, status=400)


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
            return JsonResponse({'Error': 'Missing fields in the request payload or empty, ' + str(e)}, status=400)

        if not user_id:
            return JsonResponse({'Error': 'Missing user id key in the request payload'}, status=400)

        if not job_name:
            return JsonResponse({'Error': 'Missing job name key in the request payload'}, status=400)

        if not url_data:
            return JsonResponse({'Error': 'Missing urls key in the request payload'}, status=400)

        if not project_name:
            return JsonResponse({'Error': 'Missing project_name key in the request payload'}, status=400)

        if not crawler_name:
            return JsonResponse({'Error': 'Missing crawler_name key in the request payload'}, status=400)

        if not schedule_type:
            return JsonResponse({'Error': 'Missing schedule_type key in the request payload'}, status=400)

        if (schedule_type != SCHEDULE_TASK_TYPE) \
                and (schedule_type != INTERVAL_TASK_TYPE) and (schedule_type != HOT_TASK_TYPE):
            return JsonResponse({'Error': 'Requested crawler_type:' + schedule_type + ' is not a valid type'},
                                status=400)

        publish_url_ids = []
        for url in url_data:
            if not is_valid_url(url):
                return JsonResponse({'Error': url + ' URL is invalid'}, status=400)

            unique_id = str(uuid4())  # create a unique ID.
            publish_data = u'{ "unique_id": "' + unique_id + '", "job_name": "' + job_name \
                           + '", "url": "' + url + '", "project_name": "' \
                           + project_name + '", "user_id": "' + user_id + '", "crawler_name": "' + crawler_name \
                           + '", "task_id":"" }'

            publish_data = json.loads(publish_data)
            try:
                # schedule data with celery task scheduler
                if schedule_type == SCHEDULE_TASK_TYPE:
                    publish_data['schedule_data'] = schedule_data
                    publish_data['schedule_category'] = CRON
                    publish_data['status'] = "RUNNING"
                    celery_task = schedule_job_with_cron_tab(publish_data)
                elif schedule_type == INTERVAL_TASK_TYPE:
                    publish_data['schedule_data'] = schedule_data
                    publish_data['schedule_category'] = INTERVAL
                    publish_data['status'] = "RUNNING"
                    celery_task = schedule_job_with_interval(publish_data)
                else:
                    publish_data['schedule_category'] = INSTANT
                    publish_data['status'] = "PENDING"
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
                    return JsonResponse({'Error': 'Error while connecting to the MongoDB database, ' + str(e)},
                                        status=400)
            except Exception as e:
                return JsonResponse({'Status': "400 BAD",
                                     'Error': 'Error occurred while scheduling the data with the Celery executor, '
                                              + str(e)}, status=400)

        return JsonResponse({'status': "SUCCESS", 'Message': "Crawl job scheduled successfully.\n job_ids:"
                                                             + str(publish_url_ids)})


@csrf_exempt
@require_http_methods(['POST'])  # only post
def get_crawl_data(request):
    # take urls comes from client.
    try:
        json_data = json.loads(request.body)
    except JSONDecodeError as e:
        return JsonResponse({'Error': 'Missing URLs in the request payload or empty, ' + str(e)}, status=400)

    if "user_id" not in json_data:
        return JsonResponse({'Error': 'Missing user id key in the request payload'}, status=400)

    if "task_id" not in json_data:
        return JsonResponse({'Error': 'Missing task id key in the request payload'}, status=400)

    if "unique_id" not in json_data:
        return JsonResponse({'Error': 'Missing unique id key in the request payload'}, status=400)

    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("crawled_data", json_data)
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting project details from the database, ' + str(e)}, status=400)

    return JsonResponse({'Status': "SUCCESS", 'data': json_data})


@csrf_exempt
@require_http_methods(['POST'])  # only post
def get_job_data(request):
    # take urls comes from client.
    try:
        json_data = json.loads(request.body)
    except JSONDecodeError as e:
        return JsonResponse({'Error': 'Missing URLs in the request payload or empty, ' + str(e)}, status=400)

    if "user_id" not in json_data:
        return JsonResponse({'Error': 'Missing user id key in the request payload'}, status=400)

    if ("task_id" not in json_data) and ("unique_id" not in json_data):
        return JsonResponse({'Error': 'Missing unique_id or task_id key in the request payload'}, status=400)

    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("jobs", json_data)
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting project details from the database, ' + str(e)}, status=400)

    return JsonResponse({'Status': "SUCCESS", 'data': json_data})


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_crawl_job(request, job_id):
    if request.method == 'DELETE':
        try:
            mongo_connection = MongoConnection()
            json_data = mongo_connection.get_items("jobs", {'unique_id': job_id})
            if len(json_data) == 0:
                return JsonResponse({'Error': 'Requested job id' + str(job_id) + 'does not exists'}, status=400)

            # this should be a interval or cron job
            celery_task_name = ""
            if len(json_data) > 1:
                for obj in json_data:
                    if 'celery_task_name' in obj:
                        celery_task_name = obj['celery_task_name']
                        break

            delete_count = 0
            if json_data[0]['schedule_category'] == INSTANT:
                delete_count = mongo_connection.delete_items("jobs", {'unique_id': job_id})
            else:
                # delete scheduled task from django beat
                if not celery_task_name:
                    celery_task_name = json_data[0]['celery_task_name']
                delete_schedule_job(celery_task_name)
                delete_count = mongo_connection.delete_items("jobs", {'unique_id': job_id})
            if delete_count == 0:
                return JsonResponse({'Error': 'Delete action failed for the job_id: ' + str(job_id)}, status=400)

        except Exception as e:
            return JsonResponse({'Error': 'Error while deleting the job from the database, ' + str(e)}, status=400)

        return JsonResponse({'Status': "SUCCESS", 'Message': 'Crawl job deleted successfully'})


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_crawl_task(request, task_id):
    if request.method == 'DELETE':
        try:
            mongo_connection = MongoConnection()
            delete_count = mongo_connection.delete_items("jobs", {'task_id': task_id})
            if delete_count == 0:
                return JsonResponse({'Error': 'Delete action failed for the task_id: ' + str(task_id)}, status=400)

        except Exception as e:
            return JsonResponse({'Error': 'Error while deleting the job from the database, ' + str(e)}, status=400)

        return JsonResponse({'Status': "SUCCESS", 'Message': 'Crawl job deleted successfully'})

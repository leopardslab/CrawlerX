from json import JSONDecodeError
from uuid import uuid4
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.clients.mongo_connection import MongoConnection
import json

from main.rabbitmq_sender import publish_data_to_broker


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True


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
        except JSONDecodeError as e:
            return JsonResponse({'Error': 'Missing URLs in the request payload or empty, ' + str(e)})

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
                # send data to the RabbitMQ Queue through a sender
                publish_data_to_broker(publish_data)
                publish_url_ids.append(unique_id)

                try:
                    # store job records in MongoDB database
                    query = {'user_id': user_id, 'job_name': job_name, 'url': url,
                             'project_name': project_name, 'crawler_name': crawler_name}
                    mongo_connection = MongoConnection()
                    mongo_connection.upsert_item(query, publish_data, "jobs")
                except Exception as e:
                    return JsonResponse({'Error': 'Error while connecting to the MongoDB database, ' + str(e)})
            except Exception as e:
                return JsonResponse({'status': "500 BAD", 'Exception': 'Can not publish data to the broker, ' + str(e)})

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


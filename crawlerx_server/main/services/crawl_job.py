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
            project_id = json_data['project_id']
            user_id = json_data['user_id']
        except JSONDecodeError as e:
            return JsonResponse({'Error': 'Missing URLs in the request payload or empty, ' + str(e)})

        if not user_id:
            return JsonResponse({'Error': 'Missing user id key in the request payload'})

        if not url_data:
            return JsonResponse({'Error': 'Missing urls key in the request payload'})

        if not project_id:
            return JsonResponse({'Error': 'Missing project_name key in the request payload'})

        publish_url_ids = []
        for url in url_data:
            if not is_valid_url(url):
                return JsonResponse({'error': url + ' URL is invalid'})

            unique_id = str(uuid4())  # create a unique ID.
            publish_data = '{ "unique_id": ' + unique_id + ', "url":' + url + ', "project_id": ' \
                           + project_id + ', "user_id": ' + user_id + ' }'

            try:
                # send data to the RabbitMQ Queue through a sender
                publish_data_to_broker(publish_data)
                publish_url_ids.append(unique_id)

                try:
                    # store job records in MongoDB database
                    job_record = '{ "unique_id": ' + unique_id + ', "url":' + url + ', "project_id": ' \
                           + project_id + ', "user_id": ' + user_id + ', "status": "PENDING" }'
                    mongo_connection = MongoConnection()
                    mongo_connection.upsert_item(job_record, "jobs")
                except Exception as e:
                    return JsonResponse({'Error': 'Error while connecting to the MongoDB database, ' + str(e)})
            except Exception as e:
                return JsonResponse({'status': "500 BAD", 'Exception': 'Can not publish data to the broker, ' + str(e)})

        return JsonResponse({'status': "SUCCESS", 'job_ids': publish_url_ids})

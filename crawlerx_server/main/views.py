from json import JSONDecodeError
from uuid import uuid4
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        # take urls comes from client.
        try:
            json_data = json.loads(request.body)
            url_data = json_data['urls']
            project_name = json_data['project_name']
        except JSONDecodeError:
            return JsonResponse({'Error': 'Missing URLs in the request payload or empty'})

        if not url_data:
            return JsonResponse({'Error': 'Missing urls key in the request payload'})

        if not project_name:
            return JsonResponse({'Error': 'Missing project_name key in the request payload'})

        publish_url_ids = []
        for url in url_data:
            if not is_valid_url(url):
                return JsonResponse({'error': url + ' URL is invalid'})

            unique_id = str(uuid4())  # create a unique ID.
            publish_data = '{ "unique_id": ' + unique_id + ', "url":' + url + ', "project_name": ' + project_name + ' }'

            try:
                publish_data_to_broker(publish_data)
                publish_url_ids.append(unique_id)
            except:
                return JsonResponse({'status': "500 BAD", 'Exception': 'Can not publish data to the broker'})

        return JsonResponse({'status': "SUCCESS", 'job_ids': publish_url_ids})


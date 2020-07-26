from json import JSONDecodeError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.clients.mongo_connection import MongoConnection
from scrapyd_api import ScrapydAPI
import json

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

@csrf_exempt
@require_http_methods(['GET'])  # only get and post
def get_jobs(request):
    # take urls comes from client.
    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("jobs", "sssss")
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting job details from the database, ' + str(e)})

    return JsonResponse({'status': "SUCCESS", 'data': json_data})

@csrf_exempt
@require_http_methods(['GET'])  # only get and post
def get_jobs(request):
    # take urls comes from client.
    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("jobs", "sssss")
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting job details from the database, ' + str(e)})

    return JsonResponse({'status': "SUCCESS", 'data': json_data})

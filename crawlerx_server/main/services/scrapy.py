from json import JSONDecodeError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.clients.mongo_connection import MongoConnection
import json


@csrf_exempt
@require_http_methods(['POST'])  # only get and post
def get_jobs(request):
    try:
        json_data = json.loads(request.body)
    except JSONDecodeError as e:
        return JsonResponse({'Error': 'Missing user_id in the request payload or empty, ' + str(e)}, status=400)

    # take urls comes from client.
    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("jobs", json_data)
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting job details from the database, ' + str(e)}, status=400)

    return JsonResponse({'Status': "SUCCESS", 'data': json_data})


@csrf_exempt
@require_http_methods(['POST'])  # only get and post
def get_jobs_by_project(request):
    try:
        json_data = json.loads(request.body)
        user_id = json_data['user_id']
        project_name = json_data['project_name']
    except JSONDecodeError as e:
        return JsonResponse({'Error': 'Missing user_id in the request payload or empty, ' + str(e)}, status=400)

    if not user_id:
        return JsonResponse({'Error': 'Request payload does not contain user_id'}, status=400)

    if not project_name:
        return JsonResponse({'Error': 'Request payload does not contain project_name'}, status=400)

    # take urls comes from client.
    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("jobs", {'user_id': user_id, 'project_name': project_name})
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting job details from the database, ' + str(e)}, status=400)

    return JsonResponse({'Status': "SUCCESS", 'data': json_data})


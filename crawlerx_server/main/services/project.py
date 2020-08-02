from json import JSONDecodeError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from main.clients.firebase_auth import FirebaseAuth
from main.clients.mongo_connection import MongoConnection
import json


@csrf_exempt
@require_http_methods(['POST'])  # only get and post
def project_create(request):
    # take urls comes from client.
    try:
        json_data = json.loads(request.body)
        user_id = json_data['user_id']
        project_name = json_data['project_name']
        if not user_id:
            return JsonResponse({'Error': 'Request payload does not contain user_id'})

        if not project_name:
            return JsonResponse({'Error': 'Request payload does not contain project_name'})

    except JSONDecodeError:
        return JsonResponse({'Error': 'Request payload does not contain required parameters or empty'})

    # user Authorization
    authorization_header = request.headers.get('Authorization')
    auth = FirebaseAuth(authorization_header, user_id)
    if not auth:
        return JsonResponse({'Error': 'User authentication failed. Please try again with a valid user login'})

    try:
        mongo_connection = MongoConnection()
        data_item = dict(json_data)
        query = {'user_id': data_item['user_id'], 'project_name': data_item['project_name']}
        mongo_connection.upsert_item(query, data_item, "projects")
    except Exception as e:
        return JsonResponse({'Error': 'Error while connecting to the MongoDB database, ' + str(e)})

    return JsonResponse({'status': "SUCCESS", 'message': 'project created successfully'})

@csrf_exempt
@require_http_methods(['GET'])  # only get and post
def get_projects(request):
    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("projects", "sssss")
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting project details from the database, ' + str(e)})

    return JsonResponse({'status': "SUCCESS", 'data': json_data})

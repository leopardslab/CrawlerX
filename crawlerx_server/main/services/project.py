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
        project_description = json_data['project_description']
        if not user_id:
            return JsonResponse({'Error': 'Request payload does not contain user_id'})

        if not project_name:
            return JsonResponse({'Error': 'Request payload does not contain project_name'})

        if not project_description:
            return JsonResponse({'Error': 'Request payload does not contain project_description'})

    except JSONDecodeError:
        return JsonResponse({'Error': 'Request payload does not contain required parameters or empty'})

    # user Authorization
    token_header = request.headers.get('Token')
    print(token_header)
    auth = FirebaseAuth(token_header, user_id)
    print(auth)
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
@require_http_methods(['POST'])  # only get and post
def get_projects(request):

    try:
        json_data = json.loads(request.body)
        user_id = json_data['user_id']
        if not user_id:
            return JsonResponse({'Error': 'Request payload does not contain user_id'})

    except JSONDecodeError:
        return JsonResponse({'Error': 'Request payload does not contain required parameters or empty'})

    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("projects", {'user_id': user_id})
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting project details from the database, ' + str(e)})

    return JsonResponse({'status': "SUCCESS", 'data': json_data})

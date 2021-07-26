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
            return JsonResponse({'Error': 'Request payload does not contain user_id'}, status=400)

        if not project_name:
            return JsonResponse({'Error': 'Request payload does not contain project_name'}, status=400)

    except JSONDecodeError:
        return JsonResponse({'Error': 'Request payload does not contain required parameters or empty'}, status=400)

    # user Authorization
    token_header = request.headers.get('Token')
    auth = FirebaseAuth(token_header, user_id)

    if not auth:
        return JsonResponse({'Error': 'User authentication failed. Please try again with a valid user login'},
                            status=400)

    try:
        mongo_connection = MongoConnection()
        data_item = dict(json_data)
        query = {'user_id': data_item['user_id'], 'project_name': data_item['project_name']}
        mongo_connection.upsert_item(query, data_item, "projects")
    except Exception as e:
        return JsonResponse({'Error': 'Error while connecting to the MongoDB database, ' + str(e)}, status=400)

    return JsonResponse({'status': "SUCCESS", 'Message': 'Project:' + project_name + ' created successfully'})


@csrf_exempt
@require_http_methods(['POST'])  # only get and post
def get_projects(request):

    try:
        json_data = json.loads(request.body)
        user_id = json_data['user_id']
        if not user_id:
            return JsonResponse({'Error': 'Request payload does not contain user_id'}, status=400)

    except JSONDecodeError:
        return JsonResponse({'Error': 'Request payload does not contain required parameters or empty'}, status=400)

    try:
        mongo_connection = MongoConnection()
        json_data = mongo_connection.get_items("projects", {'user_id': user_id})
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting project details from the database, ' + str(e)}, status=400)

    return JsonResponse({'Status': "SUCCESS", 'data': json_data})

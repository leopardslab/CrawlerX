from json import JSONDecodeError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.clients.elasticsearch_connection import ELKConnection
import json


@csrf_exempt
@require_http_methods(['POST'])  # only get and post
def get_elasticsearch_data(request):

    try:
        json_data = json.loads(request.body)
        user_id = json_data['user_id']
        query = json_data['query']

        if not user_id:
            return JsonResponse({'Error': 'Request payload does not contain user_id'}, status=400)

        if not query:
            return JsonResponse({'Error': 'Request payload does not contain query'}, status=400)

    except JSONDecodeError:
        return JsonResponse({'Error': 'Request payload does not contain required parameters or empty'}, status=400)

    try:
        elk_connection = ELKConnection()
        query = query.replace("\'", "\"")
        query = json.loads(query)
        json_data = elk_connection.get_data_from_query(user_id.lower(), query)
    except Exception as e:
        return JsonResponse({'Error': 'Error while getting job details from the ELK server, ' + str(e)}, status=400)

    return JsonResponse({'Status': "SUCCESS", 'data': json_data})
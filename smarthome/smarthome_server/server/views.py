import json

from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.views import View

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class ServerView(View):

    def get(self, request):
        with open('data.json', 'r') as f:
            data = json.load(f)
        if data['cold_water'] == False:
            data['boiler_temperature'] = None
        prepared_data = {
            'status': 'ok', 
            'data': [{'name': key, 'value': data[key]} for key in data]
        }
        return JsonResponse(prepared_data)

    def post(self, request):
        with open('data.json', 'r') as f:
            data = json.load(f)
            # data = {item['name']: item['value'] for item in saved_data}
        loaded_data = json.loads(request.body)['controllers']
        for item in loaded_data:
            data[item['name']] = item['value']
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        prepared_data = {
            'status': 'ok', 
            'data': [{'name': key, 'value': data[key]} for key in data]
        }
        print(data)
        return JsonResponse(prepared_data)

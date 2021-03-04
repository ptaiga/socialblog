import requests
import json

from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from django.conf import settings

from .models import Setting
from .form import ControllerForm


# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# @method_decorator(csrf_exempt, name='dispatch')
class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')
    data = {}

    def get(self, request):
        # print('Call "get" method')
        try:
            return super(ControllerView, self).get(request)
        except (JSONDecodeError, ConnectionError):
            return JsonResponse(
                {'error': 'The server does not respond or returns an error!'}, 
                status=502)

    def get_context_data(self, **kwargs):
        # print('Call "get_context_data" method')
        context = super(ControllerView, self).get_context_data(**kwargs)
        # headers = {'Authorization': f'Bearer {settings.SMART_HOME_ACCESS_TOKEN}'}
        # url = settings.SMART_HOME_API_URL
        # data = requests.get(url, headers=headers).json()['data']
        # context['data'] = {item['name']: item['value'] for item in data}
        # self.data = context['data']
        context['data'] = self.data
        return context

    def get_initial(self):
        # print('Call "get_initial" method')
        headers = {'Authorization': f'Bearer {settings.SMART_HOME_ACCESS_TOKEN}'}
        url = settings.SMART_HOME_API_URL
        try:
            r = requests.get(url, headers=headers).json()
            if r['status'] != 'ok':
                raise JSONDecodeError
            data = r['data']
        except (JSONDecodeError, ConnectionError) as err:
            raise err

        initial_data = {
            'bedroom_target_temperature': 
                Setting.objects.get(
                    controller_name='bedroom_target_temperature'
                ).value,
            'hot_water_target_temperature': 
                Setting.objects.get(
                    controller_name='hot_water_target_temperature'
                ).value,
        }

        self.data = {item['name']: item['value'] for item in data}
        initial_data['bedroom_light'] = self.data['bedroom_light']
        initial_data['bathroom_light'] = self.data['bathroom_light']
        return initial_data

    def form_valid(self, form):
        # print('Call "form_valid" method')
        br_temp = Setting.objects.get(
            controller_name='bedroom_target_temperature')
        br_temp.value = form.cleaned_data['bedroom_target_temperature']
        br_temp.save()
        hw_temp = Setting.objects.get(
            controller_name='hot_water_target_temperature')
        hw_temp.value = form.cleaned_data['hot_water_target_temperature']
        hw_temp.save()

        headers = {'Authorization': f'Bearer {settings.SMART_HOME_ACCESS_TOKEN}'}
        url = settings.SMART_HOME_API_URL
        data = {'controllers': []}
        for key in ['bedroom_light', 'bathroom_light']:
            if self.data[key] != form.cleaned_data[key]:
                data['controllers'].append({
                    'name': key, 
                    'value': form.cleaned_data[key]
                })

        res = requests.post(url, headers=headers, data=json.dumps(data))
        print(res, data)
        return super(ControllerView, self).form_valid(form)

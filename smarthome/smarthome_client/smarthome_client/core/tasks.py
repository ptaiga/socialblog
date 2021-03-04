from __future__ import absolute_import, unicode_literals

import json
import requests
from celery import task

from json.decoder import JSONDecodeError

from django.conf import settings
from django.core.mail import send_mail

from .models import Setting


MESSAGE_SENDED_FLAG = False


def send(subject='Test', content='Hi!'):
    if send_mail(subject, content, settings.EMAIL_HOST_USER, 
        [settings.EMAIL_RECEPIENT],
        fail_silently=False, auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD
    ):
        print(f"Email to '{settings.EMAIL_RECEPIENT}' send")
        return True
    else:
        print(f"Email to '{settings.EMAIL_RECEPIENT}' doesn't send. Try again later")
        return False

@task()
def smart_home_manager():
    headers = {'Authorization': f'Bearer {settings.SMART_HOME_ACCESS_TOKEN}'}
    url = settings.SMART_HOME_API_URL
    try:
        r = requests.get(url, headers=headers).json()
        if r['status'] != 'ok':
            raise JSONDecodeError
        data = r['data']
    except (JSONDecodeError, KeyError):
        return {'error': 'The server does not respond or returns an error!'}
    items = {}
    for item in data:
        items[item['name']] = item['value']
    items_old = items.copy()

    br_temp = Setting.objects.get(
        controller_name='bedroom_target_temperature').value
    hw_temp = Setting.objects.get(
        controller_name='hot_water_target_temperature').value

    if items['leak_detector']:
        items['cold_water'] = False
        items['hot_water'] = False
        global MESSAGE_SENDED_FLAG
        if not MESSAGE_SENDED_FLAG:
            if send('Leak detector!', 'Signal from the leak detector'):
                MESSAGE_SENDED_FLAG = True
    else:
        MESSAGE_SENDED_FLAG = False

    if not items['cold_water']:
        items['boiler'] = False
        items['washing_machine'] = 'off'
    else:
        if items['boiler_temperature'] \
            and items['boiler_temperature'] < (hw_temp * 0.9):
            items['boiler'] = True

        if items['boiler_temperature'] \
            and items['boiler_temperature'] > (hw_temp * 1.1):
            items['boiler'] = False

    if items['curtains'] != 'slightly_open' \
    and items['outdoor_light'] < 50 \
    and not items['bedroom_light']:
        items['curtains'] = 'open'

    if items['curtains'] != 'slightly_open' \
    and (items['outdoor_light'] >= 50 \
    or items['bedroom_light']):
        items['curtains'] = 'close'

    if items['smoke_detector']:
        items['air_conditioner'] = False
        items['bedroom_light'] = False
        items['bathroom_light'] = False
        items['boiler'] = False
        items['washing_machine'] = 'off'
        # send('Smoke detector!', 'Signal from the smoke detector!')

    if items['bedroom_temperature'] > (br_temp * 1.1) \
    and not items['smoke_detector']:
        items['air_conditioner'] = True

    if items['bedroom_temperature'] < (br_temp * 0.9):
        items['air_conditioner'] = False

    data = {'controllers': 
        [{'name': key, 'value': items[key]} for key in items
        if items[key] != items_old[key]]}

    if data['controllers']:
        requests.post(url, headers=headers, data=json.dumps(data))
    
    return data
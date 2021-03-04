from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarthome_client.settings')
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
django.setup()


app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from smarthome_client.core.tasks import smart_home_manager

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, smart_home_manager.s(), name='Check Smart Home')

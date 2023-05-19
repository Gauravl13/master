from __future__ import absolute_import,unicode_literals
import os

from celery import Celery
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Assignment2.settings')

app = Celery('Assignment2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'sync-data-every-five-minutes': {
        'task': 'empapp.tasks.sync_data_task',
        'schedule': timedelta(minutes=5)}}

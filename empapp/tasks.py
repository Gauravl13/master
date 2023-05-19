from __future__ import absolute_import,unicode_literals
from celery import shared_task
from django.core.management import call_command


@shared_task
def sync_data_task():
    call_command('sync_data')
    print('data sync from Postgre to Elastic search')


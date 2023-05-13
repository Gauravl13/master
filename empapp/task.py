from celery import shared_task
from django.core.management import call_command


@shared_task
def sync_data_task():
    call_command('sync_data')


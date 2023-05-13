from celery import Celery
from django.conf import settings

app = Celery('empapp')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

import os
from django.core.management import call_command

call_command('python manage.py sync_data')
os.system('python manage.py crontab run')
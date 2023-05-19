from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess



subprocess.call(['python', 'manage.py', 'sync_data'], bufsize=0)
class Command(BaseCommand):
    help = 'Sync data every 5 minutes using apscheduler'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(subprocess.call, 'interval', args=(['python', 'manage.py', 'sync_data'],), minutes=5)
        scheduler.start()

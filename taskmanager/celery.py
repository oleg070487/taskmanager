import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

app = Celery('taskmanager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


#  celery beat tasks
app.conf.beat_schedule = {
    'add-every-3-minutes': {
        'task': 'myapp.tasks.schedule_notifications',
        'schedule': crontab(minute='*/3'),
    },
}


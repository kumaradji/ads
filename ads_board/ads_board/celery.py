import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ads_board.settings')

app = Celery('ads_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_email_every_monday_8am': {
        'task': 'ads_board.tasks.send_email',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
    # 'send_email_every_30': {
    #     'task': 'ads_board.tasks.send_email',
    #     'schedule': timedelta(seconds=30),
    #     'args': (),
    # },
}

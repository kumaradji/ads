import os
from ads.tasks.tasks import send_response_email

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ads_board.settings')

app = Celery('ads')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_email_every_monday_8am': {
        'task': 'ads.tasks.tasks.send_email',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
    'send_email_every_30': {
        'task': 'ads.tasks.tasks.send_email',
        'schedule': 30.0,
        'args': (),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

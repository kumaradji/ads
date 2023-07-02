import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ads_board.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# рассылка подписчикам списка публикаций за неделю
# каждый понедельник в 8:00 через tasks.py
app.conf.beat_schedule = {
    'send_email_every_monday_8am': {
        'task': 'ads.tasks.send_email',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
    'send_email_every_30': {
        'task': 'ads.tasks.send_email',
        'schedule': 30.0,
        'args': (),
    },
}

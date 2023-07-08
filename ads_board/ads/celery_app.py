import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ads_board.settings')

app = Celery('ads')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

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
#
# # Создание экземпляра объекта Celery
# celery_app = Celery('my_project')
#
# # Настройка Celery
# celery_app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Загрузка задач из приложений Django
# celery_app.autodiscover_tasks()

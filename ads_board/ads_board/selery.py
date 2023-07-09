import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ads_board.settings')

app = Celery('ads_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
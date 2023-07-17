import os
from celery import Celery
from celery.schedules import crontab

# Set the 'DJANGO_SETTINGS_MODULE' environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ads_board.settings')

# Create a Celery instance
app = Celery('ads_board')

# Configure Celery using the Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in the app
app.autodiscover_tasks()

# Configure the Celery beat schedule
app.conf.beat_schedule = {
    'send_email_every_monday_8am': {
        'task': 'ads_board.tasks.send_email',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}

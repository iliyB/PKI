import os
from celery import Celery, platforms
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
platforms.C_FORCE_ROOT = True

app = Celery(
    'settings', backemd='amqp', broker=settings.CELERY_BROKER_URL
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
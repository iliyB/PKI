import os
from celery import Celery, platforms
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
platforms.C_FORCE_ROOT = True

app = Celery(
    'settings', backemd='amqp', broker=settings.CELERY_BROKER_URL,
    include=['cert.rest_tasks']
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'send-key-for-client': {
        'task': 'cert.rest_tasks.send_key_reg',
        'schedule': crontab(minute='*/1'),
    },
    'send-key-for-registration': {
        'task': 'cert.rest_tasks.send_key_cli',
        'schedule': crontab(minute='*/1'),
    }
}


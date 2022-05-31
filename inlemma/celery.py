from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inlemma.settings')

app = Celery('inlemma')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'update-D2Vmodel-every-night': {
        'task': 'spaces.updateD2Vmodel',
        'schedule': crontab(hour=0, minute=0)
    },
}

# load task modules from all registered Django app configs.
app.autodiscover_tasks()
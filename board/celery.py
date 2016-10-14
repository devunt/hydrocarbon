import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hydrocarbon.settings.production')

from django.conf import settings

app = Celery('hydrocarbon')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.BROKER_URL = 'redis://localhost:6379/0'
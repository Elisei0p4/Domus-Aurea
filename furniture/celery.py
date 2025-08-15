import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture.settings.development')

app = Celery('furniture')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()
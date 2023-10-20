import os
from celery import Celery


CELERY_BROKER_URL = 'redis://redis:6379/2'
CELERY_RESULT_BACKEND = 'redis://redis:6379/4'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_orders.settings')

app = Celery('django_celery',
             backend=CELERY_RESULT_BACKEND,
             broker=CELERY_BROKER_URL)

app.autodiscover_tasks()

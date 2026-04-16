import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Test_task_dZENcode.settings')

app = Celery('Test_task_dZENcode')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
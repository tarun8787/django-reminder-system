import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobtracker.settings')
app = Celery('jobtracker')
app.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
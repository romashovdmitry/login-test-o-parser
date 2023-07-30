import os
from celery import Celery

# standart code for Celery in Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_parser.settings')
app = Celery('test_parser')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.django.settings")

app = Celery("demo")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "watch_this.django.settings")

app = Celery("watch-this")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

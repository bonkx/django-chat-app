import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dash.settings")

# Create default Celery app
app = Celery()

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Dja ngo app configs.
app.autodiscover_tasks()

app.conf.timezone = "Asia/Jakarta"
# app.conf.beat_schedule = {
#     # Executes every minute
#     "task-get-data-iot": {
#         "task": "iot.task_celery.test",
#         # 'schedule': crontab(minute='*/2'),
#         "schedule": 20,
#         "args": (),
#     },
# }


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

from celery import Celery
from celery.schedules import crontab

from config import settings

celery_app = Celery(
    "worker", broker=settings.BROKER_URL, backend=settings.RESULT_BACKEND
)

celery_app.conf.beat_schedule = {
    "Status updater for tasks": {
        "task": "app.api_v1.tasks.celery_tasks.update_status_for_task",
        "schedule": crontab("0", "0"),
    },
    "Status updater for idps": {
        "task": "app.api_v1.idps.celery_tasks.update_status_for_idp",
        "schedule": crontab("0", "1"),
    },
}

celery_app.autodiscover_tasks(
    ["app.api_v1.tasks", "app.api_v1.idps"], related_name="celery_tasks"
)

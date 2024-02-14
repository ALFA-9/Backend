from celery import Celery
from celery.schedules import crontab

from config import settings

celery_app = Celery(
    "worker", broker=settings.BROKER_URL, backend=settings.RESULT_BACKEND
)

celery_app.conf.beat_shedule = {
    "Status updater for tasks": {
        "task": "app.api_v1.tasks.celery_tasks.update_status_for_task",
        "schedule": crontab("0", "0"),
    },
    "Status updater for idps": {
        "task": "app.api_v1.idps.celery_tasks.update_status_for_idp",
        "schedule": crontab("0", "1"),
    },
    # "Send emails for directors": {
    #     "task": "users.celery_tasks.send_daily_email",
    #     "schedule": crontab("0", "15"),
    # },
}

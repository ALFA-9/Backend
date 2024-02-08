import datetime as dt

from celery import shared_task

from tasks.models import Task


@shared_task
def update_status_for_task():
    """Обновлем статус для просроченных задач."""
    tasks = list(
        Task.objects.filter(status_progress="in_work", end_date__lt=dt.date.today())
    )
    for _, task in enumerate(tasks):
        task.statis_idp = "not_completed"
    Task.objects.bulk_update(tasks, ["status_progress"])
    return None

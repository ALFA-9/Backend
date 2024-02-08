import datetime as dt

from celery import shared_task
from django.db.models import Max

from idps.models import Idp


@shared_task
def update_status_for_idp():
    """Обновляем статус ИПР, если последняя задача просрочилась."""
    idps = list(
        Idp.objects.annotate(latest_task_end_date=Max("task__date_end")).filter(
            status_idp="in_work", latest_task_end_date__lt=dt.date.today()
        )
    )
    for _, idp in enumerate(idps):
        idp.statis_idp = "not_completed"
    Idp.objects.bulk_update(idps, ["status_idp"])
    return None

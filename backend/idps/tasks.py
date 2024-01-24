import datetime as dt

from alpha_project.celery import app
from idps.models import Idp


@app.task
def update_status_for_idp():
    idps = list(
        Idp.objects.filter(status_idp="in_work", date_end__lt=dt.date.today())
    )
    for _, idp in enumerate(idps):
        idp.statis_idp = "not_completed"
    Idp.objects.bulk_update(idps, ["status_idp"])
    return None

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP_SSL

from sqlalchemy import and_, select

from app.database.models import Employee
from config import settings


def get_all_childs_id(parent_id):
    # найти все дочерние элементы
    included = (
        select(Employee.id).where(Employee.director_id == parent_id).cte(recursive=True)
    )
    # собрать все id этих элементов
    included = included.union_all(
        select(Employee.id).where(Employee.director_id == included.c.id)
    )
    return included


def get_all_parents_id(child_id):
    included = (
        select(Employee.director_id).where(Employee.id == child_id).cte(recursive=True)
    )

    included = included.union_all(
        select(Employee.director_id).filter(
            and_(
                Employee.id == included.c.director_id,
                Employee.director_id.is_not(None),
            )
        )
    )

    return included


async def send_email(subject, message, to, file=None):
    if not settings.EMAILS_ENABLED:
        return
    msg = MIMEMultipart()
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["To"] = to
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(message))
    if file:
        for f in file:
            part = MIMEApplication(await f.read(), Name=f.filename)
            part["Content-Disposition"] = 'attachment; filename="%s"' % f.filename
            msg.attach(part)

    server = SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

    server.sendmail(settings.EMAILS_FROM_EMAIL, to, msg.as_string())
    server.close()

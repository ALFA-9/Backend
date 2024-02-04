import datetime as dt

from celery import shared_task
from django.core.mail import EmailMessage

from users.models import Email
from tasks.models import Task


@shared_task(name="send_mail")
def send_mail():
	emails = Email.objects.all()
	count = 0
	for email_db in emails:
		count += 1
		email = EmailMessage(
			subject=email_db.subject,
			body=email_db.body,
			to=[email_db.to],
		)
		email.send()
		email_db.delete()
	print(f"Отправлено {count} писем")


@shared_task(name="update_status_for_tasks")
def update_status_for_tasks():
	tasks = list(
        Task.objects.filter(status_progress="in_work",
							date_end__lt=dt.date.today())
    )
	for _, task in enumerate(tasks):
		task.status_progress = "not_completed"
	Task.objects.bulk_update(tasks, ["status_progress"])
	return None

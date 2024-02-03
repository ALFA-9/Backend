from celery import shared_task
from django.core.mail import EmailMessage

from users.models import Email


@shared_task(name="send_mail")
def send_mail():
	emails = Email.objects.all()
	for email_db in emails:
		email = EmailMessage(
			subject=f"Задача {email_db.subject}",
			body=f"Задача '{email_db.body}' завершена",
			to=[email_db.to],
		)
		email.send()
		email_db.delete()

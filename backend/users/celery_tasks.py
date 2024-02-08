from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags

from users.models import Employee


@shared_task
def send_daily_email():
    """Отправляем email и обнуляем значение в базе данных."""
    emps_with_notifications = Employee.objects.exclude(email_notifications=None)
    for emp in emps_with_notifications:
        send_mail(
            subject="Сервис ИПР",
            message=strip_tags(emp.email_notifications),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[emp.email],
            html_message=emp.email_notifications,
        )
        emp.email_notifications = None
    Employee.objects.bulk_update(emps_with_notifications, ["email_notifications"])
    return None

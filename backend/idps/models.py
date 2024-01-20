from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Idp(models.Model):
    class IdpStatus(models.TextChoices):
        IN_WORK = "in_work", _("в работе")
        CANCELED = "canceled", _("отменен")
        UNDONE = "not_completed", _("не выполнен")
        DONE = "done", _("выполнен")

    title = models.CharField(max_length=100, verbose_name="название")
    employee = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
        verbose_name="сотрудник",
        related_name="idp_employee",
    )
    director = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
        verbose_name="директор",
        related_name="idp_director",
    )
    status_idp = models.CharField(
        max_length=100,
        choices=IdpStatus.choices,
        default=IdpStatus.IN_WORK,
        verbose_name="статус",
    )
    date_start = models.DateField(verbose_name="дата начала")
    date_end = models.DateField(verbose_name="дата окончания")

    class Meta:
        verbose_name = "ИПР"
        ordering = ["id"]
        unique_together = ["title", "employee", "date_start"]

    def __str__(self):
        return self.title


class Request(models.Model):
    title = models.CharField(max_length=100, verbose_name="название")
    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, verbose_name="сотрудник"
    )
    letter = models.TextField(verbose_name="письмо")

    class Meta:
        verbose_name = "запрос на ИПР"
        verbose_name_plural = "Запросы на ИПР"
        ordering = ["id"]

    def __str__(self):
        return self.title


class Employee(models.Model):
    name = models.CharField(max_length=50)

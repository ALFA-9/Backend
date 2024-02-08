from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import TreeForeignKey

from alpha_project.constants import MAX_LENGTH_STATUS, MAX_LENGTH_TITLE
from users.models import Employee

User = get_user_model()


class Idp(models.Model):
    "Модель ИПР."

    class IdpStatus(models.TextChoices):
        IN_WORK = "in_work", _("в работе")
        CANCELLED = "cancelled", _("отменен")
        NOT_COMPLETED = "not_completed", _("не выполнен")
        DONE = "done", _("выполнен")

    title = models.CharField(max_length=MAX_LENGTH_TITLE, verbose_name=_("название"))
    employee = TreeForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("сотрудник"),
        related_name="idp_employee",
    )
    director = TreeForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("директор"),
        related_name="idp_director",
        null=True,
    )
    status_idp = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=IdpStatus.choices,
        default=IdpStatus.IN_WORK,
        verbose_name=_("статус"),
    )
    date_start = models.DateTimeField(
        verbose_name=_("дата начала"),
        default=timezone.now,
    )

    class Meta:
        verbose_name = _("индивидуальный план развития")
        ordering = ["date_start", "id"]
        unique_together = ["title", "employee", "date_start"]

    def __str__(self):
        return self.title

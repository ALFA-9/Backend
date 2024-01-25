from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import TreeForeignKey

from users.models import Employee

User = get_user_model()


class Idp(models.Model):
    class IdpStatus(models.TextChoices):
        IN_WORK = "in_work", _("в работе")
        CANCELED = "canceled", _("отменен")
        UNDONE = "not_completed", _("не выполнен")
        DONE = "done", _("выполнен")

    title = models.CharField(max_length=100, verbose_name=_("название"))
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
        max_length=100,
        choices=IdpStatus.choices,
        default=IdpStatus.IN_WORK,
        verbose_name=_("статус"),
    )
    # TODO подумать все таки о datetime?
    date_start = models.DateField(
        verbose_name=_("дата начала"), editable=False, default=date.today
    )
    date_end = models.DateField(verbose_name=_("дата окончания"))

    class Meta:
        verbose_name = _("индивидуальный план развития")
        ordering = ["date_start", "id"]
        unique_together = ["title", "employee", "date_start"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_end__gt=models.F("date_start")),
                name="check_start_date",
            ),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.date_start >= self.date_end:
            raise ValidationError(
                {
                    "date_end": _(
                        "Дата окончания должна быть больше даты начала."
                    )
                }
            )

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import TreeForeignKey

from users.models import Employee

User = get_user_model()


class Idp(models.Model):
    class IdpStatus(models.TextChoices):
        IN_WORK = "in_work", _("в работе")
        CANCELLED = "cancelled", _("отменен")
        NOT_COMPLETED = "not_completed", _("не выполнен")
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
    date_start = models.DateTimeField(
        verbose_name=_("дата начала"),
        # auto_now_add=True,
        default=timezone.now,
    )

    class Meta:
        verbose_name = _("индивидуальный план развития")
        ordering = ["date_start", "id"]
        unique_together = ["title", "employee", "date_start"]

    def __str__(self):
        return self.title

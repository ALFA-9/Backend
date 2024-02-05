from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from alpha_project.constants import (MAX_LENGTH_COMMENT, MAX_LENGTH_STATUS,
                                     MAX_LENGTH_TITLE)
from idps.models import Idp
from users.models import Employee

User = get_user_model()


class Type(models.Model):
    """Тип задачи."""

    name = models.CharField(
        verbose_name=_("Название типа задачи"),
        max_length=MAX_LENGTH_TITLE,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("Тип задачи")
        verbose_name_plural = _("Типы задач")

    def __str__(self):
        return self.name


class Control(models.Model):
    """Методы контроля выполнения задачи."""

    title = models.CharField(
        verbose_name=_("Метод контроля выполнения задачи"),
        max_length=MAX_LENGTH_TITLE,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = _("Метод контроля")
        verbose_name_plural = _("Методы контроля")

    def __str__(self):
        return self.title


class Task(models.Model):
    """Задача."""

    class ProgresStatus(models.TextChoices):
        IN_WORK = "in_work", _("в работе")
        DONE = "done", _("выполнено")
        NOT_COMPLETED = "not_completed", _("не выполнено")
        CANCELLED = "cancelled", _("отменено")

    name = models.CharField(
        verbose_name=_("Название задачи"),
        max_length=MAX_LENGTH_TITLE,
    )
    description = models.TextField(
        verbose_name=_("Описание задачи"),
    )
    idp = models.ForeignKey(
        Idp,
        related_name="task_idp",
        verbose_name=_("ИПС"),
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        Type,
        related_name="task_type",
        verbose_name=_("Тип задачи"),
        on_delete=models.CASCADE,
    )
    status_progress = models.CharField(
        verbose_name=_("Статус выполнения"),
        max_length=MAX_LENGTH_STATUS,
        choices=ProgresStatus.choices,
        default=ProgresStatus.IN_WORK,
    )
    is_completed = models.BooleanField(
        verbose_name=_("Статус работы сотрудника"),
        default=False,
    )
    control = models.ForeignKey(
        Control,
        related_name="task_control",
        verbose_name=_("Метод контроля выполнения задачи"),
        on_delete=models.CASCADE,
    )
    date_start = models.DateField(
        verbose_name=_("Дата начала выполнения задачи"),
        default=timezone.now,
    )
    date_end = models.DateField(
        verbose_name=_("Дата окончания выполнения задачи"),
    )

    class Meta:
        ordering = ("id",)
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")
        unique_together = ["name", "idp"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.date_start >= self.date_end:
            raise ValidationError(
                {
                    "date_end": _(
                        "Дата окончания должна быть больше даты начала.",
                    ),
                }
            )


class Comment(models.Model):
    """Комментарии к задаче."""

    task = models.ForeignKey(
        Task,
        related_name="comment_task",
        verbose_name=_("Задача"),
        on_delete=models.CASCADE,
    )
    employee = models.ForeignKey(
        Employee,
        related_name="comment_employee",
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
    )
    body = models.TextField(
        verbose_name=_("Комментарий"),
        max_length=MAX_LENGTH_COMMENT,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")

    def __str__(self):
        return self.body

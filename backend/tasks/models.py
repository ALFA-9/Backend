from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from idps.models import Idps

User = get_user_model()


class Type(models.Model):
    """Тип задачи."""

    name = models.CharField(
        verbose_name="Название типа задачи",
        max_length=256,
    )


class Control(models.Model):
    """Методы контроля выполнения задачи."""

    title = models.CharField(
        verbose_name="Метод контроля выполнения задачи",
        max_length=256,
    )


class Task(models.Model):
    """Задача."""

    IN_WORKE = "in_worke"
    DONE = "done"
    STATUS_PROGRESS = (
        (IN_WORKE, "in_worke"),
        (DONE, "done"),
    )
    NOT_ACCEPTED = "not_accepted"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    STATUS_ACCEPTED = (
        (NOT_ACCEPTED, "not_accepted"),
        (ACCEPTED, "accepted"),
        (CANCELLED, "cancelled"),
    )
    name = models.CharField(
        verbose_name="Название задачи",
        max_length=256,
    )
    description = models.TextField(
        verbose_name="Описание задачи",
        max_length=500,
    )
    idp = models.ForeignKey(
        Idps,
        related_name="idps_task",
        verbose_name="ИПС",
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        Type,
        related_name="type_task",
        verbose_name="Тип задачи",
        on_delete=models.CASCADE,
    )
    status_progress = models.CharField(
        verbose_name="Статус выполнения",
        max_length=20,
        choices=STATUS_PROGRESS,
        default=IN_WORKE,
    )
    status_accept = models.CharField(
        verbose_name="Статус проверки",
        max_length=20,
        choices=STATUS_PROGRESS,
        default=IN_WORKE,
    )
    control = models.ForeignKey(
        Control,
        related_name="control_task",
        verbose_name="Метод контроля выполнения задачи",
        on_delete=models.CASCADE,
    )
    date_start = models.DateTimeField(
        verbose_name="Время начала выполнения задачи",
        default=timezone.now,
    )
    date_end = models.DateTimeField(
        verbose_name="Время окончания выполнения задачи",
        default=timezone.now,
    )


class Comment(models.Model):
    """Комментарии к задаче."""

    task = models.ForeignKey(
        Task,
        related_name="task_comment",
        verbose_name="Задача",
        on_delete=models.CASCADE,
    )
    employee = models.ForeignKey(
        User,
        related_name="user_comment",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    body = models.TextField(
        verbose_name="Комментарий",
        max_length=500,
    )

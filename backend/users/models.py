from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from .constants import MAX_EMAIL_CHARACTERS, MAX_NAME_CHARACTERS
from .validators import validator_tel


class BaseEmployeeOptions(models.Model):
    """Базовая модель для сущностей Employee."""

    title = models.CharField("Заголовок", max_length=MAX_NAME_CHARACTERS)

    class Meta:
        abstract = True
        ordering = ("id",)

    def __str__(self):
        return self.title


class Grade(BaseEmployeeOptions):
    """Модель грейда."""

    class Meta(BaseEmployeeOptions.Meta):
        verbose_name = "Грейд"
        verbose_name_plural = "Грейды"


class Post(BaseEmployeeOptions):
    """Модель должности."""

    class Meta(BaseEmployeeOptions.Meta):
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Department(BaseEmployeeOptions):
    """Модель подразделения."""

    class Meta(BaseEmployeeOptions.Meta):
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"


class Employee(MPTTModel):
    """Класс работников."""

    first_name = models.CharField("Имя", max_length=MAX_NAME_CHARACTERS)
    last_name = models.CharField("Фамилия", max_length=MAX_NAME_CHARACTERS)
    patronymic = models.CharField("Отчество", max_length=MAX_NAME_CHARACTERS)
    phone = models.CharField(
        "Номер телефона",
        max_length=MAX_NAME_CHARACTERS,
        unique=True,
        validators=(validator_tel,),
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Грейд",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Должность",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Подразделение",
    )
    director = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="employees",
        verbose_name="Руководитель",
    )

    class MPTTMeta:
        parent_attr = "director"

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class User(AbstractUser):
    """Класс пользователей."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "password")

    email = models.EmailField(
        "E-mail", max_length=MAX_EMAIL_CHARACTERS, unique=True
    )
    employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE, null=True
    )

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from .constants import MAX_EMAIL_CHARACTERS, MAX_NAME_CHARACTERS
from .managers import CustomUserManager
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


class Employee(MPTTModel, AbstractBaseUser, PermissionsMixin):
    """Класс работников."""

    first_name = models.CharField("Имя", max_length=MAX_NAME_CHARACTERS)
    last_name = models.CharField("Фамилия", max_length=MAX_NAME_CHARACTERS)
    patronymic = models.CharField("Отчество", max_length=MAX_NAME_CHARACTERS)
    image = models.ImageField("Фото", upload_to="profiles/",
                              null=True, default="profiles/default_pic.jpeg")
    email = models.EmailField(
        "E-mail",
        max_length=MAX_EMAIL_CHARACTERS,
        unique=True,
    )
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
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class MPTTMeta:
        parent_attr = "director"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def get_full_name(self):
        full_name = "%s %s %s" % (
            self.last_name,
            self.first_name,
            self.patronymic,
        )
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"

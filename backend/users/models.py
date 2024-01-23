from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validator_tel
from .constants import MAX_EMAIL_CHARACTERS, MAX_NAME_CHARACTERS

class BaseEmployeeOptions(models.Model):
    """ Модель грейда. """

    title = models.CharField("Заголовок", max_length=MAX_NAME_CHARACTERS)

    class Meta:
        abstract = True
        ordering = ("id",)

    def __str__(self):
        return self.title


class Grade(BaseEmployeeOptions):
    """ Модель грейда. """

    class Meta(BaseEmployeeOptions.Meta):
        verbose_name = "Грейд"
        verbose_name_plural = "Грейды"


class Post(models.Model):
    """ Модель должности. """

    class Meta(BaseEmployeeOptions.Meta):
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Department(models.Model):
    """ Модель подразделения. """

    class Meta(BaseEmployeeOptions.Meta):
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"


class User(AbstractUser):
    """ Класс пользователей/работников. """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "password", "first_name", "last_name")

    username = models.CharField(
        'Логин',
        max_length=MAX_NAME_CHARACTERS,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким именем уже есть',
        }
    )
    email = models.EmailField("E-mail", max_length=MAX_EMAIL_CHARACTERS,
                              unique=True)
    first_name = models.CharField("Имя",
                                  max_length=MAX_NAME_CHARACTERS)
    last_name = models.CharField("Фамилия",
                                 max_length=MAX_NAME_CHARACTERS)
    patronymic = models.CharField("Отчество",
                                 max_length=MAX_NAME_CHARACTERS)
    phone = models.CharField("Номер телефона", max_length=MAX_NAME_CHARACTERS,
                             unique=True, validators=(validator_tel,))
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    director = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"
        ordering = ("last_name",)
        default_related_name = 'user_set'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

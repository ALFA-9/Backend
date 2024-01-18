from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

User = get_user_model()


class Idp(models.Model):
    class IdpStatus(models.TextChoices):
        IN_WORK = 'in_work', _('в работе')
        CANCELED = 'canceled', _('отменен')
        UNDONE = 'undone', _('не выполнен')
        DONE = 'done', _('выполнен')
    title = models.CharField(max_length=100,
                             verbose_name='название')
    # employee = models.ForeignKey('Employee', on_delete=models.CASCADE,
    #                              verbose_name='сотрудник', related_name='idps_employee')
    # director = models.ForeignKey('Employee', on_delete=models.CASCADE,
    #                              verbose_name='директор', related_name='idps_director')
    # status_idp = models.CharField(choices=IdpStatus.choices, default=IdpStatus.IN_WORK,
    #                               verbose_name="статус")

    class Meta:
        verbose_name = 'ИПР'
        ordering = ['id']

    def __str__(self):
        return self.title


class Request(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='название')
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE,
                                 verbose_name='сотрудник')
    letter = models.TextField(verbose_name="письмо")

    class Meta:
        verbose_name = 'запрос на ИПР'
        verbose_name_plural = 'Запросы на ИПР'
        ordering = ['id']

    def __str__(self):
        return self.title


class Employee(models.Model):
    class Departaments(models.TextChoices):
        dep1 = '1', _('1 отдел')
        dep2 = '2', _('2 отдел')
        dep3 = '3', _('3 отдел')
    name = models.CharField(max_length=50, verbose_name="Имя")
    departament = models.CharField(choices=Departaments.choices, verbose_name="отдел")
    is_director = models.BooleanField(default=False)
    #director = models.ForeignKey('Employee', blank=True, on_delete=models.DO_NOTHING, default=None)

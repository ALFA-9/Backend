from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin
from rest_framework.authtoken.models import TokenProxy

from .models import Department, Employee, Grade, Post


@admin.register(Employee)
class EmployeeAdmin(MPTTModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "patronymic")
    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "email",
                    "phone",
                )
            },
        ),
        (
            _("Служебная информация"),
            {"fields": ("grade", "post", "department", "director")},
        ),
    )
    empty_value_display = "-пусто-"


admin.site.register(Grade)
admin.site.register(Post)
admin.site.register(Department)
admin.site.unregister(Group)

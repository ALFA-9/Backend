import os

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin

from .models import Department, Employee, Grade, Post


@admin.register(Employee)
class EmployeeAdmin(MPTTModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "patronymic")
    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "preview",
                    "image",
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
    search_fields = ("^first_name", "^last_name", "^patronymic")

    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(
            f'<img src="{os.getenv("HOST_URL", "http://localhost:8000")}'
            f'/media/{obj.image}" style="max-height: 200px;">'
        )


admin.site.register(Grade)
admin.site.register(Post)
admin.site.register(Department)
admin.site.unregister(Group)

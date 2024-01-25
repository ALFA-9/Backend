from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Department, Employee, Grade, Post, User


@admin.register(Employee)
class EmployeeAdmin(MPTTModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "patronymic",
        "phone",
        "grade",
        "post",
        "department",
        "director",
    )
    empty_value_display = "-пусто-"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "employee",
    )
    empty_value_display = "-пусто-"


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    empty_value_display = "-пусто-"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    empty_value_display = "-пусто-"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    empty_value_display = "-пусто-"

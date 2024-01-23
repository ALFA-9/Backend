from django.contrib import admin

from .models import Comment, Control, Task, Type


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "idp",
        "type",
        "status_progress",
        "status_accept",
        "control",
        "date_start",
        "date_end",
    )
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "task",
        "employee",
        "body",
        "pub_date",
    )
    empty_value_display = "-пусто-"


@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    empty_value_display = "-пусто-"


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    empty_value_display = "-пусто-"

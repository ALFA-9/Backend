from django.contrib import admin

from tasks.models import Comment, Task, TaskControl, TaskType


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "idp",
        "type",
        "status_progress",
        "is_completed",
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


@admin.register(TaskControl)
class ControlAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    empty_value_display = "-пусто-"


@admin.register(TaskType)
class TypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    empty_value_display = "-пусто-"

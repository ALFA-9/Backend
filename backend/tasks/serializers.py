import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Comment, Control, Task, Type


class TypeSerializer(serializers.ModelSerializer):
    """Сереализатор типов задач."""

    class Meta:
        model = Type
        fields = (
            "id",
            "name",
        )


class ControlSerializer(serializers.ModelSerializer):
    """Сереализатор типов задач."""

    class Meta:
        model = Control
        fields = (
            "id",
            "title",
        )


class CommentTaskSerializer(serializers.ModelSerializer):
    """Сереализатор комментариев к задачам."""

    employee = serializers.SerializerMethodField()
    employee_post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "employee",
            "employee_post",
            "body",
            "pub_date",
        )

    def get_employee(self, obj):
        """ФИО работника."""
        employee = obj.employee
        employee = (
            f"{employee.last_name} {employee.first_name} {employee.patronymic}"
        )
        return employee

    def get_employee_post(self, obj):
        """Должность работника."""
        return obj.employee.post.title


class TaskGetSerializer(serializers.ModelSerializer):
    """Сереализатор задач."""

    comments = CommentTaskSerializer(many=True, source="comment_task")
    type = serializers.StringRelatedField(source="type.name")
    control = serializers.StringRelatedField(source="control.title")

    class Meta:
        model = Task
        fields = (
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
            "comments",
        )

        extra_kwargs = {
            "date_start": {"input_formats": ["%Y-%m-%d", "%d.%m.%Y"]},
            "date_end": {"input_formats": ["%Y-%m-%d", "%d.%m.%Y"]},
        }

    def to_representation(self, instance):
        instance.date_start = instance.date_start.strftime("%d.%m.%Y")
        instance.date_end = instance.date_end.strftime("%d.%m.%Y")

        return super().to_representation(instance)


class TaskSerializer(serializers.ModelSerializer):
    """Сереализатор задач."""

    class Meta:
        model = Task
        fields = (
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

    def to_representation(self, instance):
        serializer = TaskGetSerializer(instance)
        return serializer.data

    def validate_date_end(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError(
                _("Дата окончания должна быть больше даты начала.")
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сереализатор комментариев."""

    class Meta:
        model = Comment
        fields = (
            "id",
            "task",
            "employee",
            "body",
            "pub_date",
        )

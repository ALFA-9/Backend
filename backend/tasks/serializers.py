import datetime as dt

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework import serializers

from tasks.models import Comment, Control, Task, Type


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

    employee = serializers.StringRelatedField()
    employee_post = serializers.StringRelatedField(source="employee.post")
    employee_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "employee",
            "employee_image",
            "employee_post",
            "body",
            "pub_date",
        )

    def get_pub_date(self, value):
        return value

    def get_employee_image(self, value):
        relative_url = value.employee.image.url
        return relative_url


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
            "is_completed",
            "control",
            "date_start",
            "date_end",
            "comments",
        )


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
            "is_completed",
            "control",
            "date_start",
            "date_end",
        )

    def to_representation(self, instance):
        serializer = TaskGetSerializer(instance)
        return serializer.data

    def validate_date_start(self, value):
        if value < dt.date.today():
            raise serializers.ValidationError(
                _("Нельзя создать задачу задним числом.")
            )
        return value

    def validate_date_end(self, value):
        if value < dt.date.today():
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


class CurrentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "date_end",
        )


class TaskForIdpSerializer(serializers.ModelSerializer):
    date_start = serializers.DateField()

    class Meta:
        model = Task
        exclude = ("idp",)

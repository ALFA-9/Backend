import datetime as dt

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from idps.models import Idp
from tasks.models import Comment, Task
from tasks.serializers import TaskSerializer
from users.models import Employee


def create_tasks(data, model):
    for task_data in data:
        task_data["idp"] = model
        Task.objects.create(**task_data)


class TaskForIdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ("idp",)


class EmployeeForIdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
        )


class CurrentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "date_end",
        )


class IdpWithCurrentTaskSerializer(serializers.ModelSerializer):
    current_task = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    director = EmployeeForIdpSerializer()
    tasks = TaskSerializer(many=True, source="task_idp")

    class Meta:
        model = Idp
        fields = (
            "id",
            "title",
            "progress",
            "current_task",
            "director",
            "tasks",
        )

    def get_current_task(self, obj):
        current_task = (
            obj.task_idp.filter(
                status_progress="in_work", date_end__gt=dt.date.today()
            )
            .order_by("date_start")
            .first()
        )
        if not current_task:
            return None
        return CurrentTaskSerializer(current_task).data

    def get_progress(self, obj):
        tasks_not_canceled_count = obj.task_idp.exclude(
            status_accept="canceled"
        ).count()
        if not tasks_not_canceled_count:
            return None
        tasks_done_count = obj.task_idp.filter(
            status_accept="accepted"
        ).count()
        return tasks_done_count / tasks_not_canceled_count * 100


class IdpSerializer(serializers.ModelSerializer):
    employee = EmployeeForIdpSerializer()
    director = EmployeeForIdpSerializer()

    class Meta:
        model = Idp
        fields = (
            "id",
            "title",
            "employee",
            "director",
            "status_idp",
            "date_start",
            "date_end",
        )


class CreateIdpSerializer(serializers.ModelSerializer):
    tasks = TaskForIdpSerializer(many=True, source="task_idp")

    class Meta:
        model = Idp
        fields = (
            "id",
            "title",
            "employee",
            "director",
            "status_idp",
            "tasks",
            "date_start",
            "date_end",
        )

    def validate_date_end(self, value):
        if value <= dt.date.today():
            raise serializers.ValidationError(
                _("Дата окончания должна быть больше даты начала.")
            )
        return value

    def create(self, validated_data):
        tasks_data = validated_data.pop("task_idp")
        idp = Idp.objects.create(**validated_data)
        create_tasks(tasks_data, idp)
        return idp


class RequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    letter = serializers.CharField()
    director_id = serializers.IntegerField()
    file = serializers.FileField(required=False)


class CommentSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField()
    employee_post = serializers.StringRelatedField(
        source="employee.post.title"
    )

    class Meta:
        model = Comment
        fields = ("id", "employee", "employee_post", "body", "pub_date")


class TaskWithComments(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, source="comment_task")
    type = serializers.StringRelatedField(source="type.name")
    control = serializers.StringRelatedField(source="control.title")

    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            "type",
            "control",
            "status_progress",
            "status_accept",
            "date_start",
            "date_end",
            "comments",
        )


class IdpWithAllTasksWithComments(serializers.ModelSerializer):
    tasks = TaskWithComments(many=True, source="task_idp")

    class Meta:
        model = Idp
        fields = ("title", "employee", "director", "status_idp", "tasks")

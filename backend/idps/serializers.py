import datetime as dt

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from idps.models import Idp
from tasks.models import Task
from tasks.serializers import (CurrentTaskSerializer, TaskForIdpSerializer,
                               TaskGetSerializer)
from users.models import Employee


def create_tasks(data, model):
    for task_data in data:
        task_data["idp"] = model
        Task.objects.create(**task_data)


class EmployeeForIdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
        )


class IdpWithCurrentTaskSerializer(serializers.ModelSerializer):
    current_task = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    director = serializers.StringRelatedField()

    class Meta:
        model = Idp
        fields = (
            "id",
            "director",
            "title",
            "progress",
            "status_idp",
            "current_task",
        )

    def get_current_task(self, obj) -> CurrentTaskSerializer:
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

    def get_progress(self, obj) -> int:
        tasks_not_canceled_count = obj.task_idp.exclude(
            status_progress="cancelled"
        ).count()
        if not tasks_not_canceled_count:
            return None
        tasks_done_count = obj.task_idp.filter(status_progress="done").count()
        return int(tasks_done_count / tasks_not_canceled_count * 100)


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
        )

    def validate_tasks(self, value):
        print(value)
        for task in value:
            if task["date_start"] < dt.date.today():
                raise serializers.ValidationError(
                    _("Нельзя создать задачу задним числом.")
                )
            elif task["date_start"] >= task["date_end"]:
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

    def to_representation(self, instance):
        instance["file"] = instance["file"].name
        return instance


class IdpWithAllTasksWithComments(serializers.ModelSerializer):
    tasks = TaskGetSerializer(many=True, source="task_idp")

    class Meta:
        model = Idp
        fields = ("title", "employee", "director", "status_idp", "tasks")


class CreateIdpScheme(CreateIdpSerializer):
    class Meta:
        model = Idp
        fields = (
            "id",
            "title",
            "employee",
            "status_idp",
            "tasks",
        )

from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Сереализатор тегов."""

    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            # "idp,
            "type",
            "status_progress",
            "status_accept",
            "control",
            "date_start",
            "date_end",
        )

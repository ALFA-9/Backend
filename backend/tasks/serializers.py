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


class TaskGetSerializer(serializers.ModelSerializer):
    """Сереализатор задач."""

    comments = serializers.SerializerMethodField()
    type = TypeSerializer()
    control = ControlSerializer()

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

    def get_comments(self, obj):
        """Сообщения."""
        comments = obj.comment_task.all()
        return CommentSerializer(comments, many=True).data

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


class CommentSerializer(serializers.ModelSerializer):
    """Сереализатор комментариев к задачам."""

    class Meta:
        model = Comment
        fields = (
            "id",
            "task",
            "employee",
            "body",
            "pub_date",
        )

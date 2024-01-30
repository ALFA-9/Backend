from rest_framework import serializers

from .constants import MAX_DEPTH
from .models import Employee


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""

    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "phone",
            "grade",
            "post",
            "department",
            "is_staff",
        )


class DirectorSerializer(EmployeeSerializer):
    """Сериализатор для кастомной модели пользователя."""

    subordinates = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "phone",
            "grade",
            "post",
            "department",
            "subordinates",
            "is_staff",
        )

    def get_subordinates(self, director):
        return EmployeeSerializer(director.get_descendants(
            include_self=False).filter(level__lte=director.level + MAX_DEPTH),
            many=True).data

from rest_framework import serializers

from .models import Employee


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmployeeSerializer(serializers.ModelSerializer):
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
        return director.get_descendants(include_self=False).values_list(
            "email", flat=True
        )

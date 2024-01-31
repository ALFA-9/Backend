from rest_framework import serializers

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

    def __init__(self, *kwrgs, max_depth):
        self.max_depth = max_depth
        super().__init__(*kwrgs)

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
        if self.max_depth > 1:
            serializer = DirectorSerializer(
                director.get_descendants(include_self=False).filter(
                    level__lte=director.level + self.max_depth
                ),
                max_depth=self.max_depth - 1,
                many=True,
            )
            return serializer.data

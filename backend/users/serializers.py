from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """ Сериализатор для кастомной модели пользователя. """

    subordinates = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ("id", "username", "first_name", "last_name", "patronymic",
                  "email", "phone", "grade", "post", "department",
                  "director", "subordinates", "is_staff")

    def get_subordinates(self, director):
        return director.get_descendants(include_self=False)

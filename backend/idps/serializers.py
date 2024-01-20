from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from idps.models import Employee, Idp

ru_error_messages = {
    "does_not_exist": _(
        'Недопустимый первичный ключ "{pk_value}"' " - объект не существует."
    ),
}


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "name",
        )


class IdpSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(required=True)
    director = EmployeeSerializer(required=True)

    class Meta:
        model = Idp
        fields = (
            "title",
            "employee",
            "director",
            "status_idp",
            "date_start",
            "date_end",
        )


class CreateIdpSerializer(serializers.ModelSerializer):
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

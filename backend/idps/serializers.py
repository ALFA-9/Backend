import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from idps.models import Employee, Idp


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "name",
            "email",
        )


class IdpSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    director = EmployeeSerializer()

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
        extra_kwargs = {
            "date_start": {"input_formats": ["%Y-%m-%d", "%d.%m.%Y"]},
            "date_end": {"input_formats": ["%Y-%m-%d", "%d.%m.%Y"]},
        }

    def to_representation(self, instance):
        instance.date_start = instance.date_start.strftime("%d.%m.%Y")
        instance.date_end = instance.date_end.strftime("%d.%m.%Y")
        return super().to_representation(instance)


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
        extra_kwargs = {
            "date_start": {"input_formats": ["%Y-%m-%d", "%d.%m.%Y"]},
            "date_end": {"input_formats": ["%Y-%m-%d", "%d.%m.%Y"]},
        }

    def to_representation(self, instance):
        instance.date_start = instance.date_start.strftime("%d.%m.%Y")
        instance.date_end = instance.date_end.strftime("%d.%m.%Y")
        return super().to_representation(instance)

    def validate_date_end(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError(
                _("Дата окончания должна быть больше даты начала.")
            )
        return value


class NestedEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("name", "email")

    def get_fields(self):
        fields = super(NestedEmployeeSerializer, self).get_fields()
        fields["employee"] = NestedEmployeeSerializer(
            many=True, required=False
        )
        return fields

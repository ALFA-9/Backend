from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from idps.models import Idp, Employee

ru_error_messages = {
    'does_not_exist': _('Недопустимый первичный ключ "{pk_value}"'
                        ' - объект не существует.'),
}


class IdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idp
        fields = ('title', 'emplyee', 'director', 'status_idp',)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name', 'departament', 'director',)
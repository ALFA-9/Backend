import re

from django.core.exceptions import ValidationError

from alpha_project.constants import REGEX_TEL


def validator_tel(value):
    newstr = re.sub(REGEX_TEL, "", value)
    if newstr:
        raise ValidationError("Номер телефона введен неверно")
    return value

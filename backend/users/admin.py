from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)

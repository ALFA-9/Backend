from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Employee, User


class EmployeeAdmin(MPTTModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(User, UserAdmin)

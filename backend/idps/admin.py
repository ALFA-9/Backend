from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from idps.models import Employee, Idp

# Register your models here.
admin.site.register(Employee, MPTTModelAdmin)
admin.site.register(Idp)

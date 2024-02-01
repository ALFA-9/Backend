from django.contrib import admin

from idps.models import Idp


@admin.register(Idp)
class IdpAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "employee",
        "director",
        "status_idp",
        "date_start",
        "date_end",
    )
    empty_value_display = "-пусто-"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .labels import *

class AccountAdmin(UserAdmin):
    list_display = ("email", "username", "date_joined", "last_login", "is_admin",)
    search_fields = ("email", "username",)
    readonly_fields = ("date_joined", "last_login",)
    filter_horizontal = ("job", "instrument", "genre",)
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(User, AccountAdmin)
admin.site.register(Job)
admin.site.register(Genre)
admin.site.register(Instrument)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Maps
from django.contrib.gis.admin import OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin

from .models import *
from .labels import *

class AccountAdmin(UserAdmin, OSMGeoAdmin): # LeafletGeoAdmin || OSMGeoAdmin
    list_display = ("id", "email", "username", "date_joined", "last_login", "is_admin",)
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


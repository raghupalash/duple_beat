from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path('<int:user_id>', user_detail_view, name="index"),
    path('user_location/<int:user_id>', user_location, name="user_location"),
    path('user_location/set/<int:user_id>', set_user_location, name="set_user_location"),
    path('user_location/set/map/<int:user_id>', set_user_map_location, name="set_user_map_location"),
]
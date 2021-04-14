from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path('<int:user_id>', user_detail_view, name="index"),
    path('edit/<int:user_id>', edit_user_detail_view, name="edit_user_detail_view"),
    path('profile_photo/<int:user_id>', profile_photo, name="profile_photo"),
    path('user_location/set/<int:user_id>', set_user_location, name="set_user_location"),
]
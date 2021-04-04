from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path('<int:user_id>', user_detail_view, name="index"),
]
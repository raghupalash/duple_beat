# django imports
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, Http404

# internal imports
from .models import *

# Create your views here.

# class index(View):
def user_detail_view(request, user_id, *args, **kwargs):

    user = User.objects.get(pk=user_id)

    context = {
        "user": user,
    }

    return render(request, "users/profile.html", context)
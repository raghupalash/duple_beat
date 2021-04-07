# from django.contrib.gis import forms
from django import forms

from leaflet.forms.widgets import LeafletWidget
from .models import *


# class MyGeoForm(forms.Form):

#     point = forms.PointField(
#         widget=forms.OSMWidget(
#             attrs={
#                 'map_width': 800, 
#                 'map_height': 500
#             }
#         )
#     )

class MyGeoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('location',)
        widgets = {'location_point': LeafletWidget()}
from django.contrib.gis import forms
from leaflet.forms.fields import PointField
from leaflet.forms.widgets import LeafletWidget

from PIL import Image
from django.core.files import File

from .models import *

LEAFLET_WIDGET_ATTRS = {
    'map_height': '400px',
    'map_width': '100%',
    # 'display_raw': 'false',
    'map_srid': 4326,
    'color': 'red',
}

class LocationForm(forms.ModelForm):
    required_css_class = 'required'

    location = forms.PointField(
        widget=LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS), label='')

    class Meta:
        model = User
        fields = ('location',)

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'genre', 
            'job', 
            'instrument', 
        )
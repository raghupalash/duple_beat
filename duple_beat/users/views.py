# django imports
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

# Maps
import folium
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.core.serializers import serialize
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# internal imports
from .models import *
from .labels import *
from .forms import *

# Create your views here.

# class index(View):
def user_detail_view(request, user_id, *args, **kwargs):

    return render(request, "users/profile.html", {
        'user': User.objects.get(pk=user_id),
    })

def user_location(request, user_id, *args, **kwargs):

    message = search_address = search = point_location = None

    user = User.objects.get(pk=user_id)

    m = folium.Map(

        width = 630,
        height = 389,
        location = list(user.location)[::-1] if user.location else None, # (4.7064546, -74.0925343), # User's location | user.location
        zoom_start = 16,

    )

    if user.location:
        folium.Marker(

            list(user.location)[::-1], #[4.7064546, -74.0925343],
            tooltip = 'Your current location!',
            popup = "This is your current location.",
            icon = folium.Icon(color="blue"),

        ).add_to(m) # Remember to add marker to map.


    if request.method == "POST":
        
        geolocator = Nominatim(user_agent="users")

        search = str(request.POST["address"]).strip().replace(',', '')

        location = geolocator.geocode(search)

        while not location:

            search = " ".join(search.split()[:len(search.split()) - 1])
            location = geolocator.geocode(search)

            if not search:
                break

        if location:

            point_location = Point(location.longitude, location.latitude, srid=4326)

            m = folium.Map(

                width = 800,
                height = 500,
                location = (location.latitude, location.longitude),
                zoom_start = 16,

            )

            # m.location = (location.latitude, location.longitude)
            # m.zoom_start = 16

            folium.Marker(
                
                [location.latitude, location.longitude],
                tooltip = location.address,
                popup = 'Your searched location!',
                icon = folium.Icon(color="blue"),

            ).add_to(m) # Remember to add marker to map.

            search_address = location.address
        
        else:
            message = "No location found."

    
    return render(request, 'users/user_location.html', {

        'user': User.objects.get(pk=user_id),
        'map': m._repr_html_(), # map in html representation
        'message': message,
        'search_address': search_address,
        'search': search,
        'form': LocationForm(initial={'location': point_location if point_location else user.location}), # (request.POST or None),

    })

def set_user_location(request, user_id, *args, **kwargs):

    user = User.objects.get(pk=user_id)

    geolocator = Nominatim(user_agent="users")
    location = geolocator.geocode(request.POST["search"])

    point_location = Point(location.longitude, location.latitude, srid=4326)
    user.location = point_location
    user.address = location.address

    user.save()

    return HttpResponseRedirect(reverse('users:index', args=(user.id,)))

def set_user_map_location(request, user_id, *args, **kwargs):

    user = User.objects.get(pk=user_id)

    form = LocationForm(request.POST)

    if form.is_valid():

        point = form.cleaned_data.get('location') # point.x = is longitude | point.y is latitude

        geolocator = Nominatim(user_agent="users")

        location = geolocator.reverse(f"{point.y}, {point.x}") #("52.509669, 13.376294")

        user.location = Point(location.longitude, location.latitude, srid=4326)
        user.address = location.address

        user.save()


    return HttpResponseRedirect(reverse('users:index', args=(user.id,)))
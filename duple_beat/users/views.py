# django imports
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

# Images
from PIL import Image

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

    user = User.objects.get(pk=user_id)
    message = search_address = search = point_location = modal = None

    if request.method == "POST":
        
        modal = True
        
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
            search_address = location.address
        
        else:
            message = "No location found."

    m = folium.Map(

        max_width = 500,
        max_height = 300,
        location = list(user.location)[::-1] if user.location else None, # (location.latitude, location.longitude), # User's location | user.location
        zoom_start = 16,

    )

    if user.location:
        folium.Marker(

            list(user.location)[::-1], #[4.7064546, -74.0925343],
            tooltip = f"{user.address[:30]}...",
            popup = 'Your current location!',
            icon = folium.Icon(color="red"),

        ).add_to(m) # Remember to add marker to map.

    return render(request, "users/profile.html", {
        'modal': modal,
        'user': user,
        'map': m._repr_html_(), # map in html representation
        'message': message,
        'search_address': search_address,
        'search': search,
        'profileform': ProfileForm(
            initial={
                'genre': user.genre.all(),
                'job': user.job.all(),
                'instrument': user.instrument.all(),
            }
        ),
        'form': LocationForm(initial={'location': point_location if point_location else user.location}), # (request.POST or None),
    })

def edit_user_detail_view(request, user_id, *args, **kwargs):
    
    user = User.objects.get(pk=user_id)

    form = ProfileForm(request.POST)

    if form.is_valid():
        user.genre.set(form.cleaned_data.get('genre'))
        user.job.set(form.cleaned_data.get('job'))
        user.instrument.set(form.cleaned_data.get('instrument'))


    user.name = request.POST["name"]
    user.about = request.POST["about"]
    
    if request.POST["from"]:
        user.budget_from = int(request.POST["from"])
    
    else:
        user.budget_from = 0

    
    if request.POST["to"]:
        user.budget_to = int(request.POST["to"])
    
    else:
        user.budget_to = 0

    user.website = request.POST["website"]
    user.instagram = request.POST["instagram"]
    user.twitter = request.POST["twitter"]
    user.facebook = request.POST["facebook"]
    user.tiktok = request.POST["tiktok"]
    user.youtube = request.POST["youtube"]
    user.soundcloud = request.POST["soundcloud"]
    user.spotify = request.POST["spotify"]
    user.tidal = request.POST["tidal"]
    user.deezer = request.POST["deezer"]

    user.save()

    return HttpResponseRedirect(reverse('users:index', args=(user.id,)))

def set_user_location(request, user_id, *args, **kwargs):

    user = User.objects.get(pk=user_id)

    if request.POST["decision"] == "0":
        geolocator = Nominatim(user_agent="users")
        location = geolocator.geocode(request.POST["search"])

    else:
        form = LocationForm(request.POST)
        if form.is_valid():

            point = form.cleaned_data.get('location') # point.x = is longitude | point.y is latitude
            geolocator = Nominatim(user_agent="users")
            location = geolocator.reverse(f"{point.y}, {point.x}") #("52.509669, 13.376294")

    try:
        user.location = Point(location.longitude, location.latitude, srid=4326)
        user.address = location.address
        user.save()
    
    except:
        pass

    return HttpResponseRedirect(reverse('users:index', args=(user.id,)))


def profile_photo(request, user_id, *args, **kwargs):

    user = User.objects.get(pk=user_id)

    if request.FILES.get("image", False) != False and 'image' in request.FILES["image"].content_type:
        user.image.delete()
        user.image = request.FILES["image"]
        user.save() # Can we just pass args to save???

        img = Image.open(user.image.path)

        x = float(request.POST["x"])
        y = float(request.POST["y"])
        h = float(request.POST["h"])
        w = float(request.POST["w"])

        img = img.crop((x, y, w+x, h+y))
        img.save(user.image.path)

        if img.height != img.width:
            size = abs(img.height - img.width) // 2

            if img.height > img.width:
                area = (0, size, (img.height - (2 * size)), img.height - size)
                
            else:
                area = (size, 0, img.width - size, (img.width - (2 * size)))
            
            crop = img.crop(area)
            crop.save(user.image.path)
        
        if user.image.size > 5485760: # 5MB
            user.image.delete()
            user.image = 'default-profile.png'
            user.save()
    
    return HttpResponseRedirect(reverse('users:index', args=(user.id,)))
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
from .forms import DistanceForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import socket

# Create your views here.
def homepage(request):
    try:
        form = DistanceForm(request.POST or None)
        geolocator = Nominatim(user_agent='DistanceCalc')
        op_str = ""
        map = folium.Map(width=800, height=500 )
        if form.is_valid():
            geo = GeoIP2()
            source_ip = socket.gethostbyname(form.cleaned_data.get('source_url'))
            source_position = geo.lat_lon(source_ip)
            source_city = geo.city(source_ip)
            city_location = geolocator.geocode(source_city)
            map = folium.Map(width=800, height=500 )
            folium.Marker(source_position, tooltip='click here for more', popup=source_city['city'],
                            icon=folium.Icon(color='red', icon='cloud')).add_to(map)
            instance = form.save()
            destination_ = form.cleaned_data.get('destination')
            destination = geolocator.geocode(destination_)
            destination_position = (destination.latitude, destination.longitude)
            distance = round(geodesic(source_position, destination_position).miles, 2)
            instance.distance = distance
            instance.source =  city_location
            instance.save()
            map = folium.Map(width=800, height=500, location=destination_position)
            folium.Marker(source_position, tooltip='click here for more', popup=destination_,
                            icon=folium.Icon(color='blue', icon='cloud')).add_to(map)
            folium.PolyLine([[source_position[0], source_position[1]],
                        [destination_position[0], destination_position[1]]]).add_to(map)
            op_str = f"Source Server at {source_city['city']}. Distance from {source_city['city']} to {destination_} is {distance} miles."

        map = map._repr_html_()
        context = {
            'form': DistanceForm(),
            'map': map,
            'output' : op_str
        }
        return render(request, 'home.html', context)
    except Exception as exc:
        print(exc)
        return HttpResponse(f"Error Processing your request. Please try again later. ERROR:  {exc}")

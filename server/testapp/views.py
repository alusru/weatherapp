import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import City
from .forms import CityForm
# Create your views here.


def home(request):

    #city = 'Cape Town'
    if request.method == 'POST':
        form = CityForm(request.POST)

        form.save()
    form = CityForm()
    cities = City.objects.all()

    for citya in cities:
        print(citya.name)
        mapBox_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+citya.name + \
            ".json?access_token=pk.eyJ1IjoibWJ1c28iLCJhIjoiY2s4OGltMTN3MDhjZTNtcW1ucG9pZnplaiJ9.YxcGEm6U8eU0huEWX_katg"
    r_mb = requests.get(mapBox_url).json()
    long = str(r_mb['features'][1]['geometry']['coordinates'][0])
    lat = str(r_mb['features'][1]['geometry']['coordinates'][1])
    url = 'https://api.darksky.net/forecast/46cabea5aa954eacb8162f0b6376e7a0/'+long + ',' + lat

    data_for_the_weather = []
    cities = City.objects.all()

    for city in cities:
        r = requests.get(url).json()
        weather_result = {
            'city': city.name,
            'temperature': r['currently']['temperature'],
            'description': r['currently']['summary'],
            'wind': r['currently']['windSpeed'],
        }

        data_for_the_weather.append(weather_result)

    template = loader.get_template('testapp/index.html')
    context = {
        'data_city_weather': data_for_the_weather,
        'form': form
    }
    return HttpResponse(template.render(context, request))

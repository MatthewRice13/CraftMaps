from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from .models import Brewery_Table
import googlemaps
import simplejson

from datetime import datetime
from operator import itemgetter
from math import sin, cos, sqrt, atan2, radians

# Support Methods #
googleKey = "AIzaSyDFK8QRiUl8jx5YYQwDMQ31GMyXwXz-et8"
gmaps = googlemaps.Client(key=googleKey)


# Create your views here.
###########################################################
# Home Page
def home(request):
    context = {
        'brewery': Brewery_Table.objects.get(id=1),
        'brewery_json': buildjson(Brewery_Table.objects.all()),
        'key': googleKey
    }
    return render(request, 'homepage.html', context)


def buildjson(data):
    rtn_json = []
    count = 0
    for d in data:
        if count > 17:
            break
        count = count+1
        item = {
            'name': d.Brewery_Name,
            'coords': {
                'lat': float(d.Brewery_Longitude),
                'lng': float(d.Brewery_Latitude)
            },
            'Content': "<h1>"+d.Brewery_Type+"</h1>"
        }
        rtn_json.append(item)
    return simplejson.dumps(rtn_json, separators=(',', ':'))


################################################################
# Routes Page
def routes(request):
    starting_point = (53.2785327, -6.1899008)
    # if 'start' in request.POST:
    #     start_location = request.POST['start']
    # else:
    #     start_location = ('The Spire, North City, Dublin')
    breweries = Brewery_Table.objects.all()
    distance = []
    for location in breweries:
        latlng = (
            (float(simplejson.dumps(location.Brewery_Longitude))),
            (float(simplejson.dumps(location.Brewery_Latitude)))
        )
        if float(get_distance(starting_point, latlng)) < 20:
            distance.append([location.Brewery_Name,
                             simplejson.dumps(float(location.Brewery_Longitude)),
                             simplejson.dumps(float(location.Brewery_Latitude)),
                             location.Brewery_URL,
                             float(get_distance(starting_point, latlng))])
    distance = sorted(distance, key=itemgetter(4))
    context = {'locations': distance[:5],
               'start': list(starting_point),
               'key': googleKey
               }
    return render(request, 'routes.html', context)


# Clean distance API response
def get_distance(start, finish):
    now = datetime.now()
    try:
        if not isinstance(start, tuple):
            geocode_result = gmaps.geocode(start[0], start[1])
        else:
            geocode_result = (start[0], start[1])
        # approximate radius of earth in km
        R = 6373.1
        ##
        lat1 = radians(geocode_result[0])
        lon1 = radians(geocode_result[1])
        lat2 = radians(float(finish[0]))
        lon2 = radians(float(finish[1]))

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
    except googlemaps.exceptions.ApiError as err:
        print(err)
    return distance


#########################################################
# about page
def about(request):
    context = {

    }
    return render(request, 'about.html', context)


#########################################################
# contacts page
def contact(request):
    context = {

    }
    return render(request, 'contact.html', context)

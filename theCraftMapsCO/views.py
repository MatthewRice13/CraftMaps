from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from .models import Brewery_Table
import googlemaps
import simplejson
import pandas as pd

from datetime import datetime
from operator import itemgetter

from math import sin, cos, sqrt, atan2, radians
import numpy as np

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


# builds json for map
def buildjson(data):
    rtn_json = []
    count = 0
    start = "<h1 class='hi'>"
    end = "</h1>"
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
            'Content': '<div class="infoDiv"><div class="infoHeader"><label class="headerLabel">'+d.Brewery_Name+'</label></div><div class="infoBody"><label class="bodyLabel">'+d.Brewery_Type+'</label></div></div>'
        }
        rtn_json.append(item)
    return simplejson.dumps(rtn_json, separators=(',', ':'))


################################################################
# Routes Page
def routes(request):
    if 'value1' in request.method:
        lat = float(request.POST['value1'])
        lng = float(request.POST['value2'])
        starting_point = (lat, lng)
    else:
        starting_point = (53.3256826, -6.2249631)

    context = {'locations': builddistjson(Brewery_Table.objects.all(), starting_point),
               'start': list(starting_point),
               'key': googleKey
               }
    return render(request, 'routes.html', context)


def builddistjson(mysqldata, starting):
    breweries = mysqldata
    data = []
    df = pd.DataFrame(data, columns=['Name', 'Distance'])
    for dat in breweries:
        nam = dat.Brewery_Name
        dst = get_distance(starting, (dat.Brewery_Longitude, dat.Brewery_Latitude))
        df = df.append(pd.DataFrame([[nam, dst]], columns=['Name', 'Distance']))

    df = df.sort_values('Distance')
    subset = df.loc[:, 'Name']

    rtn_json = []
    for d in mysqldata:
        if d.Brewery_Name in subset.values[:5]:
            item = {
                'name': d.Brewery_Name,
                'coords': {
                    'lat': float(d.Brewery_Longitude),
                    'lng': float(d.Brewery_Latitude)
                },
                'Content': '<div class="infoDiv"><div class="infoHeader"><label class="headerLabel">'+d.Brewery_Name+'</label></div><div class="infoBody"><label class="bodyLabel">'+d.Brewery_Type+'</label></div><div class="infoFooter"><button onClick="getDirections('+str(d.Brewery_Longitude)+','+str(d.Brewery_Latitude)+');">See my Directions</button></div></div>'
            }
            rtn_json.append(item)

    return simplejson.dumps(rtn_json, separators=(',', ':'))


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

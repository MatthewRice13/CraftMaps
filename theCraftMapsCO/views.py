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

    for d in data:

        item = {
            'name': d.Brewery_Name,
            'coords': {
                'lng': float(d.Brewery_Longitude),
                'lat': float(d.Brewery_Latitude)
            },
            'Content': '<div class="infoDiv"><div class="infoHeader"><label class="headerLabel">'+d.Brewery_Name+'</label></div><div class="infoBody"><label class="bodyLabel">'+d.Brewery_Type+'</label></div></div>'
        }
        rtn_json.append(item)
    return simplejson.dumps(rtn_json, separators=(',', ':'))


################################################################
# Routes Page
def routes(request):
    if request.method == 'POST':
        print_test(str(request.POST.get('value1')) + "," + str(request.POST.get('value2')))
        lat = request.POST.get('value1')
        lng = request.POST.get('value2')
        starting_point = (float(lat), float(lng))
    elif request.method == 'GET':
        start = read_data('data_dump.txt')
        start = start.split(",")
        starting_point = (float(start[0]), float(start[1]))
    else:
        starting_point = (53.3256826, -6.2249631)

    context = {'locations': builddistjson(Brewery_Table.objects.all(), starting_point),
               'start': list(starting_point),
               'key': googleKey
               }
    return render(request, 'routes.html', context)


# returns brewery json
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
                'Content': '<div class="infoDiv"><div class="infoHeader"><label class="headerLabel" id = "'+d.Brewery_URL+'" onClick="showModal(event);">'+d.Brewery_Name+'</label></div><div class="infoBody"><label class="bodyLabel">'+d.Brewery_Type+'</label></div><div class="infoFooter"><button onClick="getDirections('+str(d.Brewery_Longitude)+','+str(d.Brewery_Latitude)+');">See my Directions</button></div></div>'
            }
            rtn_json.append(item)

    return simplejson.dumps(rtn_json, separators=(',', ':'))


# Clean distance API response
def get_distance(start, finish):
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


# contact page
def contact(request):
    context = {

    }
    return render(request, 'about.html', context)


#########################################################
# support methods
def print_test(test_data):
    with open("data_dump.txt", "w") as text_file:
        text_file.write(test_data)
        text_file.close()


def read_data(file):
    with open(file, 'r') as text_file:
        data = text_file.read()
        text_file.close()
        return data

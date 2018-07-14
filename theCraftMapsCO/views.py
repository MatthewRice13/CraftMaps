from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

from .models import Brewery_Table
import googlemaps
import simplejson
import pandas as pd

from datetime import datetime
from operator import itemgetter

from math import sin, cos, sqrt, atan2, radians
import numpy as np

import twitter

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


################################################################
# Routes Page
def multiRoutes(request):
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

    context = {'locations': builddistmultijson(Brewery_Table.objects.all(), starting_point),
               'start': list(starting_point),
               'key': googleKey
               }
    return render(request, 'multiRoutes.html', context)


######################################################################
def builddistmultijson(mysqldata, starting):
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
                'Content': '<div class="infoDiv"><div class="infoHeader"><label class="headerLabel" id = "'+d.Brewery_URL+'" onClick="showModal(event);">'+d.Brewery_Name+'</label></div><div class="infoBody"><label class="bodyLabel">'+d.Brewery_Type+'</label></div><div class="infoFooter"></div></div>'
            }
            rtn_json.append(item)

    return simplejson.dumps(rtn_json, separators=(',', ':'))


def print_test(test_data):
    with open("data_dump.txt", "w") as text_file:
        text_file.write(test_data)
        text_file.close()


def read_data(file):
    with open(file, 'r') as text_file:
        data = text_file.read()
        text_file.close()
        return data


#########################################################
# signup page
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



#########################################################
#Build JSON for Brewery Page
def buildBreweryJson(data):
    rtn_json = []
    item = {
        'name': data.Brewery_Name,
        'coords': {
            'lat': float(data.Brewery_Longitude),
            'lng': float(data.Brewery_Latitude)
        },
        'Content': '<div class="infoDiv"><div class="infoHeader"><label class="headerLabel">' + data.Brewery_Name + '</label></div><div class="infoBody"><label class="bodyLabel">' + data.Brewery_Town + '</label></div></div>',
    }
    rtn_json.append(item)
    return simplejson.dumps(rtn_json, separators=(',', ':'))


def buildBeerJson(data):
    rtn_json = []
    item = {
        'name': data.Beer_Name,
        'brewery': data.Beer_Brewery,
        'type': data.Beer_Type,
        'percent': data.Beer_Percent,
        'rating': data.Beer_Rating,
    }
    rtn_json.append(item)
    return simplejson.dumps(rtn_json, separators=(',', ':'))


### Twitter API info ###
consumer_key = '16iWxCzBIzdwaRusHVnUdYxLs'
consumer_secret = 'Q677oYS73EP4UFBgJfRnG1npGTfcgd1B9xbpaxBQxocxawCW5T'
access_token_key = '959052235815649280-GxbCZphkg4oUizZ4QeUwyksToEFaIiB'
access_token_secret = 'NY41FPXbM1NLmhlwXircyArfSXHUTvZqBRK668BTSVTMU'


#Get Twitter Profile Pic
def getProfilePic(handle):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
    user = api.GetUser(screen_name=handle)
    pic = user.profile_image_url.replace("_normal.jpg", ".jpg")
    return pic


# brewery page
def brewery_page(request, Brewery_Name):
    context = {
        'brewery': buildBreweryJson(Brewery_Table.objects.get(Brewery_Name=Brewery_Name)),
        'key': googleKey
    }
    return render(request, 'breweryPage.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import User_Table, Beer_Table, Brewery_Table

import googlemaps
import simplejson
import pandas as pd

from datetime import datetime
from math import sin, cos, sqrt, atan2, radians
from random import randint
import operator
import difflib
import twitter

# Support Methods #
googleKey = "AIzaSyDFK8QRiUl8jx5YYQwDMQ31GMyXwXz-et8"
gmaps = googlemaps.Client(key=googleKey)

### Twitter API info ###
consumer_key = '16iWxCzBIzdwaRusHVnUdYxLs'
consumer_secret = 'Q677oYS73EP4UFBgJfRnG1npGTfcgd1B9xbpaxBQxocxawCW5T'
access_token_key = '959052235815649280-GxbCZphkg4oUizZ4QeUwyksToEFaIiB'
access_token_secret = 'NY41FPXbM1NLmhlwXircyArfSXHUTvZqBRK668BTSVTMU'


# Create your views here.
###########################################################
# Home Page
def home(request):
    context = {
        'brewery': Brewery_Table.objects.get(id=1),
        'brewery_json': build_home_json(Brewery_Table.objects.all()),
        'key': googleKey
    }
    return render(request, 'homepage.html', context)


# builds json for map
def build_home_json(data):
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
# builds single route
def routes(request):
    # number of breweries displayed
    k_size = 10

    # post request
    if request.method == 'POST':
        data_saving_method(str(request.POST.get('value1')) + "," + str(request.POST.get('value2')))
        lat = request.POST.get('value1')
        lng = request.POST.get('value2')
        starting_point = (float(lat), float(lng))
    # else get
    elif request.method == 'GET':
        start = read_data('data_dump.txt')
        start = start.split(",")
        starting_point = (float(start[0]), float(start[1]))
    # else
    else:
        starting_point = (53.3256826, -6.2249631)

    context = {
        'locations': builddistjson(Brewery_Table.objects.all(), starting_point, k_size),
        'start': list(starting_point),
        'key': googleKey
    }
    return render(request, 'routes.html', context)


# builds multi route
def multiRoutes(request):
    # number of breweries displayed
    k_size = 5

    # post request
    if request.method == 'POST':
        data_saving_method(str(request.POST.get('value1')) + "," + str(request.POST.get('value2')))
        lat = request.POST.get('value1')
        lng = request.POST.get('value2')
        starting_point = (float(lat), float(lng))
    elif request.method == 'GET':
        start = read_data('data_dump.txt')
        start = start.split(",")
        starting_point = (float(start[0]), float(start[1]))
    else:
        starting_point = (53.3256826, -6.2249631)

    context = {
        'locations': builddistjson(Brewery_Table.objects.all(), starting_point, k_size),
        'start': list(starting_point),
        'key': googleKey
    }
    return render(request, 'multiRoutes.html', context)


# builds json for page
def builddistjson(breweries, starting, k):
    data = []
    for dat in breweries:
        nam = dat.Brewery_Name
        typ = dat.Brewery_Type
        rat = dat.Brewery_Rating
        dst = get_distance(starting, (dat.Brewery_Longitude, dat.Brewery_Latitude))

        # data
        data.append(
            {
                'Name': nam,
                'Type': typ,
                'Rating': rat,
                'Distance': dst
            }
        )

    # sort based on distance
    df = sorted(data, key=operator.itemgetter('Distance'))

    # filters based on user preference
    ndf = similarity_map(df, (k+k))

    # subset of data
    subset = []
    for d in ndf[:k]:
        subset.append(d['Name'])

    rtn_json = []
    for d in breweries:
        if d.Brewery_Name in subset:
            item = {
                'name': d.Brewery_Name,
                'coords': {
                    'lng': float(d.Brewery_Longitude),
                    'lat': float(d.Brewery_Latitude)
                },
                'Content': '<div class="infoDiv"><div class="infoHeader"><label class="headerLabel" id = "'+d.Brewery_URL+'" onClick="showModal(event);">'+d.Brewery_Name+'</label></div><div class="infoBody"><label class="bodyLabel">'+d.Brewery_Type+'</label></div><div class="infoFooter"><button onClick="getDirections('+str(d.Brewery_Longitude)+','+str(d.Brewery_Latitude)+');">See my Directions</button></div></div>'
            }
            rtn_json.append(item)

    # returns json
    return simplejson.dumps(rtn_json, separators=(',', ':'))


# classifies based on users preferred brewery type
def similarity_map(data, k):
    data_map = []

    # users favourite brewery type
    types_of_brewery = ["Brew Pub", "Micro Brewery", "Commercial"]

    # builds a similarity map based on user preference
    for item in data[:k]:
        # random selection of brewery
        rand = randint(0, len(types_of_brewery)-1)
        check = types_of_brewery[rand]

        # gets similarity
        similarity_result = difflib.SequenceMatcher(None, check, item['Type']).ratio()

        # finds best similarity
        data_map.append(
            {
                'Name': item['Name'],
                'Type': item['Type'],
                'Distance': item['Distance'],
                'Rating': float(item['Rating']),
                'Sim': similarity_result
             }
        )

    # sorts on distance in ASC, then by sim and rating in DESC
    data_map = sorted(data_map, reverse=False, key=operator.itemgetter('Distance'))
    rtn = sorted(data_map, reverse=True, key=operator.itemgetter('Sim', 'Rating'))

    dump_test(rtn)
    # returns data
    return rtn


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
        lon2 = radians(float(finish[0]))
        lat2 = radians(float(finish[1]))

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


######################################################################
# data logging methods
def data_saving_method(test_data):
    with open("data_dump.txt", "w") as text_file:
        text_file.write(test_data)
        text_file.close()


# reads file
def read_data(file):
    with open(file, 'r') as text_file:
        data = text_file.read()
        text_file.close()
        return data


# log file for testing
def dump_test(test_data):
    with open("log_dump.txt", "w") as text_file:
        text_file.write(str(test_data))
        text_file.close()


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
        'address': {
            'name': data.Brewery_Name,
            'location': data.Brewery_Address,
            'region': data.Brewery_Region
        },
        'brewery_type': data.Brewery_Type,
        'rating': data.Brewery_Rating,
        'social': {
            'website': data.Brewery_URL,
            'twitter': data.Brewery_Twitter,
            'facebook': data.Brewery_Facebook
        },
        'pic': getProfilePic(data.Brewery_Twitter)
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


#Get Twitter Profile Pic
def getProfilePic(handle):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
    url = handle.split("/")
    user = api.GetUser(screen_name=url[len(url)-1])
    pic = user.profile_image_url.replace("_normal.jpg", ".jpg")
    return pic


# brewery page
def brewery_page(request, Brewery_Name):
    context = {
        'brewery': buildBreweryJson(Brewery_Table.objects.get(Brewery_Name=Brewery_Name)),
        'beer': buildBeerJson(Beer_Table.objects.get(Beer_Brewery=Brewery_Name)),
        'key': googleKey
    }
    return render(request, 'breweryPage.html', context)


#####################################################################
### Signup Page ###
def signup(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        user_form = UserProfileForm(request.POST)
        if sign_up_form.is_valid() and user_form.is_valid():
            sign_up_form.save()
            user_form.save()
            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        sign_up_form = SignUpForm()
        user_form = UserProfileForm()
    return render(request, 'signup.html', {'sign_up_form': sign_up_form, 'user_form': user_form})


def buildUserJson(user_data, auth_data):
    rtn_json = []
    item = {
        'brewery_type': user_data.User_Favorite_Brewery_Type,
        'max_distance': user_data.User_Max_Distance,
        'beer':{
            'stout': user_data.User_Beer_Stout,
            'lager': user_data.User_Beer_Lager,
            'ipa': user_data.User_Beer_IPA,
            'cider': user_data.User_Beer_Cider,
            'pilsner': user_data.User_Beer_Pilsner,
            'ale': user_data.User_Beer_Ale,
            'weiss': user_data.User_Beer_Weiss
        },
        'id': auth_data.id,
        'username': auth_data.username,
        'email': auth_data.email,
        'date_joined': auth_data.date_joined
    }
    rtn_json.append(item)
    return simplejson.dumps(rtn_json, separators=(',', ':'))


### User Page ###
@login_required()
def user_page(request):
    if request.user.is_authenticated:
        user_data = User_Table.objects.get(user=request.user.id)
        auth_data = User.objects.get(id=request.user.id)
        context = {
            'user': buildBreweryJson(user_data, auth_data)
        }
        render(request, 'user.html', context)

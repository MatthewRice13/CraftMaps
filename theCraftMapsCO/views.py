from django.shortcuts import render
from .models import Brewery_Table
import googlemaps
from datetime import datetime
import simplejson

### Support Methods ###
key = 'AIzaSyDFK8QRiUl8jx5YYQwDMQ31GMyXwXz-et8'
gmaps = googlemaps.Client(key=key)

#Clean distance API response
def get_distance(start, finish):
    now = datetime.now()
    try:
        if not isinstance(start, tuple):
            geocode_result = gmaps.geocode(start[0], start[1])
        else:
            geocode_result = (start[0], start[1])
        distance_result = gmaps.distance_matrix(geocode_result, finish, mode='driving', departure_time=now)
        instructions = distance_result['rows'][0]['elements'][0]['distance']['text'][:4]
    except googlemaps.exceptions.ApiError as err:
        print(err)
    return instructions

# Create your views here.
def home(request):
    brewery = Brewery_Table.objects.get(id=1)
    context = {
        'brewery': brewery
    }
    return render(request, 'homepage.html', context)

def routes(request):
    starting_point = (53.2785327, -6.1899008)
    breweries = Brewery_Table.objects.all()
    distance = []
    for location in breweries:
        latlng = (simplejson.dumps(float(location.Brewery_Longitude)), (float(simplejson.dumps(location.Brewery_Latitude))))
        if float(get_distance(starting_point, latlng)) < 20:
            distance.append([location.Brewery_Name,
                             simplejson.dumps(float(location.Brewery_Longitude)),
                             simplejson.dumps(float(location.Brewery_Latitude)),
                             location.Brewery_URL,
                             float(get_distance(starting_point, latlng))])
    context = {'locations': distance}
    return render(request, 'routes.html', context)
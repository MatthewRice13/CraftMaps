import requests
import re, time
import urllib.request
import urllib.parse
from difflib import SequenceMatcher
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# links used
ratebeer_Ireland_URL = "https://www.ratebeer.com/breweries/ireland/0/100/#closed"


#########################
# scraping tool
# get data from links
def make_soup(url_linker):
    # impose scrape padding
    time.sleep(5.0)
    req = requests.get(url_linker)
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    return soup


########################
# parsing & cleaning
# gets table data
def parse_table(URLi):
    page = make_soup(URLi)
    page_table = page.find_all('table')[0]

    # data
    data = []
    for i, li in enumerate(page_table.select('tr')):

        # gets other data
        txt = str(i)
        for d in li.select('td'):
            if "<br/>" in str(d):
                fresh = str(d).split("<br/>")
                brewery_name = BeautifulSoup(fresh[0], "html.parser").text
                brewery_region = BeautifulSoup(fresh[1], "html.parser").text
            else:
                txt = txt + ", " + re.sub("\s\s+", " ", d.text)

        # gets url
        for ab in li.select('a'):
            brewery_url = get_brewery_url(ab['href'], brewery_name)[0]
            break

        # skip empty value
        # clean data
        if i != 0:
            # formats into array
            brewery_type = str(txt).split(", ")

            # accounts for dirt
            if "rew" not in brewery_type[0]:
                loc = find_brew_type(brewery_type)
                brewery_type = brewery_type[loc]

            # creats dict
            context = {
                'name': brewery_name,
                'region': brewery_region,
                'type': brewery_type,
                'url': brewery_url
            }
            # adds to data
            data.append(context)

    return data


# gets brewery url
def get_brewery_url(url_ending, brew_name):
    data = []
    url_brews = "https://www.ratebeer.com"
    work_url = url_brews + url_ending

    # get urls
    for link in make_soup(work_url).find_all('a'):
        lk = link.get('href')

        # check brew name to find url
        if url_similarity("http://" + brew_name + ".com", str(lk)) > 0.7:
            data.append(lk)

        # add brew to increase check
        elif url_similarity("http://" + brew_name + "brew.com", str(lk)) > 0.7:
            data.append(lk)

    # failsafe
    if len(data) <= 0:
        data.append("www.google.com")

    return data


###########################
# cleaning methods
# url similarity measure
def url_similarity(url_a, url_b):
    return SequenceMatcher(None, url_a, url_b).ratio()


# cleans address
def parseAddress(address):
    return re.sub("\s\s+", "", re.sub('"', '', re.sub('"langaddress": ', '', address)))


# coverts string to float
def parseFloat(digit):
    return float(re.findall("\d+\.\d+", digit)[0])


# removes unwanted data from html
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


# gets type from array
def find_brew_type(look_up):
    value = 0
    for i, d in enumerate(look_up):
        if "rew" in d:
            value = i

    return value


#########################
# creates dictionary
def pull_data(new_str):
    for i, d in enumerate(new_str.split("\n")):
        if "langaddress" in d:
            address = parseAddress(d)
        if "lon" in d:
            long = parseFloat(d)
        if "lat" in d:
            lat = parseFloat(d)

    # create dict
    content = {
        "address": address,
        "long": long,
        "lati": lat
    }

    # return
    return content


########################
# data entry prep
# gets long lats from nominatim
def make_data(url_link):
    url_link = url_link.replace(" ", "+")
    page = make_soup(url_link)
    section = page.find_all('script')[0]
    data = find_between(str(section), "var nominatim_results = [", "\"importance") + " }"
    return data


# cleans and formats
def complete_data():
    # url formating
    site_url = "https://nominatim.openstreetmap.org/search.php?q="
    country = "Ireland"
    ending = "&polygon_geojson=1&viewbox="
    spacing = "%2C"

    # parse table data
    table_data = parse_table(ratebeer_Ireland_URL)

    # data entry
    brew_data = []

    for z, d in enumerate(table_data):

        # testing
        if z > 1:
            break

        # gather data
        brewery_name = d['name']
        brewery_town = d['region']
        brewery_type = d['type']
        brewery_URL = d['url']

        # create failsafe
        URLA = site_url + brewery_name + brewery_town + spacing + country + ending
        URLB = site_url + brewery_town + spacing + country + ending
        newSTR = make_data(URLA)

        # check urls
        if len(newSTR) < 5:
            newSTR = make_data(URLB)
            cut_data = pull_data(newSTR)
        else:
            cut_data = pull_data(newSTR)

        # create dict for db entry
        model_dictionary = {
            'name': brewery_name,
            'address': cut_data['address'],
            'type': brewery_type,
            'lati': cut_data['lati'],
            'long': cut_data['long'],
            'url': brewery_URL
        }

        # creates dict
        brew_data.append(model_dictionary)

    # return
    return brew_data

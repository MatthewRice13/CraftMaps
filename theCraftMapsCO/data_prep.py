import requests, re, time
import urllib.request, urllib.parse
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
    time.sleep(0.5)
    req = requests.get(url_linker)
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    return soup


########################
# parsing & cleaning
# gets table data
def parse_table(URLi):
    print("Starting...")
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
            url_data = get_brewery_url(ab['href'], brewery_name)
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
                'url': url_data['url'],
                'twitter': url_data['twitter'],
                'facebook': url_data['facebook']
            }
            # adds to data
            data.append(context)

    print("table data: done...")
    return data


# gets brewery url
def get_brewery_url(url_ending, brew_name):
    time.sleep(0.2)
    data = []
    url_brews = "https://www.ratebeer.com"
    work_url = url_brews + url_ending

    # clean name
    brew_name = re.sub(" ", "", str(brew_name))
    brew_name = re.sub("-", "", str(brew_name))
    brew_name = re.sub("Brewery", "", str(brew_name))

    # get urls
    links_list = make_soup(work_url).find_all('a')

    # works all links
    for link in links_list:
        lk = link.get('href')
        lk = re.sub("www.", "", str(lk))
        lk = re.sub("https://", "", str(lk))
        lk = re.sub("http://", "", str(lk))
        # url
        # check brew name to find url
        if url_similarity("" + brew_name + ".com", str(lk)) > 0.8:
            url = lk
            break
        # add brew to increase check
        if url_similarity("" + brew_name + ".ie", str(lk)) > 0.8:
            url = lk
            break
        # add brew to increase check
        if url_similarity("" + brew_name + "brewe.com", str(lk)) > 0.7:
            url = lk
            break
        # add brew to increase check
        if url_similarity("" + brew_name + "brewe.ie", str(lk)) > 0.7:
            url = lk
            break
        # add brew to increase check
        if url_similarity("the" + brew_name + ".com", str(lk)) > 0.8:
            url = lk
            break
        # add brew to increase check
        if url_similarity("the" + brew_name + ".ie", str(lk)) > 0.8:
            url = lk
            break
        else:
            # failsafe
            url = "www.google.com"

    # twitter
    for link in links_list:
        lk = link.get('href')
        lk = re.sub("https://www.", "", str(lk))
        # check brew name to find url
        if url_similarity("twitter.com/" + brew_name + "", str(lk)) > 0.7:
            twitter = "www." + lk
            break
        # add brew to increase check
        elif url_similarity("twitter.com/" + brew_name + "brew", str(lk)) > 0.7:
            twitter = "www." + lk
            break
        else:
            # failsafe
            twitter = "www.twitter.com"

    # facebook
    for link in links_list:
        lk = link.get('href')
        lk = re.sub("https://www.", "", str(lk))
        # check brew name to find url
        if url_similarity("facebook.com/" + brew_name + "", str(lk)) > 0.7:
            facebook = re.sub("@", "", "www." + lk)
            break
        # add brew to increase check
        elif url_similarity("facebook.com/" + brew_name + "brew", str(lk)) > 0.7:
            facebook = re.sub("@", "", "www." + lk)
            break
        # add brew to increase check
        elif url_similarity("facebook.com/the" + brew_name + "", str(lk)) > 0.7:
            facebook = re.sub("@", "", "www." + lk)
            break
        # add brew to increase check
        elif url_similarity("facebook.com/pages/" + brew_name + "/", str(lk)) > 0.55:
            facebook = re.sub("@", "", "www." + lk)
            break
        else:
            # failsafe
            facebook = "www.facebook.com"

    url_content = {
        'url': url,
        'twitter': twitter,
        'facebook': facebook
    }
    return url_content


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
    rtn_flo = re.findall("\d+\.\d+", digit)
    if len(rtn_flo) >= 1:
        rtn = rtn_flo[0]
    else:
        rtn = 0.0
    return float(rtn)


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
    ads = "none"
    lon = 0.0
    lat = 0.0

    for i, d in enumerate(new_str.split("\n")):
        if "langaddress" in d:
            ads = parseAddress(d)

        if "lon" in d:
            lon = parseFloat(d)

        if "lat" in d:
            lat = parseFloat(d)

    # create dict
    content = {
        "address": ads,
        "long": lon,
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
        if z % 5 == 0:
            time.sleep(1.5)
        # gather data
        brewery_name = d['name']
        brewery_town = d['region']
        brewery_type = d['type']
        brewery_URL = d['url']
        brewery_twitter = d['twitter'],
        brewery_facebook = d['facebook']

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
            'url': brewery_URL,
            'twitter': brewery_twitter,
            'facebook': brewery_facebook
        }
        # creates dict
        brew_data.append(model_dictionary)
    # return
    print("complete data: done...")
    return brew_data


# coding: utf-8

# In[1]:


import sys,re,ast,decimal
import mysql.connector as mysql
from mysql.connector import errorcode
from mysql.connector import (connection)
from decimal import Decimal
from difflib import SequenceMatcher
# database requirements
userOf = "UserOne"
passOf = "PassOne123#"
Url = "localhost"
DataBase = "CraftMapsDB"
# similarity metric
def similar(a, b):
    a = a.lower()
    b = b.lower()
    return SequenceMatcher(None, a, b).ratio()
# loads brewery data
def get_brewery():    
    fname = "new_database.txt"
    content_data = []
    with open(fname) as f:
        #reads all lines
        for content in f.readlines():
            data = eval(content)
            content_data.append(data)
    return content_data
# cleans beer data
def get_beer():
    fname = "FULL_Beers.txt"
    UD = []
    content_data = []
    with open(fname) as f:
        #reads all lines
        for content in f.readlines():
            data=content.split(",")
            name=data[1]
            brewery=data[0]
            style=data[2]
            proof=data[3]
            rating=data[4]
            available=data[5]
            # cleaning
            name = re.sub("'","",name)
            brewery = re.sub("'","",brewery)
            brewery = re.sub(" company","",brewery)
            brewery = re.sub(" diageo","",brewery)
            brewery = re.sub(" craft","",brewery)
            brewery = re.sub(" ireland","",brewery)
            available=available.split("\n")
            # build content
            content = {
                'name':name,
                'brewery':brewery,
                'style':style,
                'proof':proof,
                'rating':rating,
                'available':available[0]
            }
            content_data.append(content)
    return content_data
# combines brewery and beer data
def data_combo():
    #size=21
    brews=get_brewery()
    beers=get_beer()
    data = []
    for brew in brews:
        brew_name = str(brew['name'])
        for beer in beers:
            beer_name = beer['brewery']
            if (similar(brew_name,beer_name) > 0.75):
                content = {
                    'name':beer['name'],
                    'brewery':brew_name.strip(),
                    'style':beer['style'],
                    'proof':beer['proof'],
                    'rating':beer['rating']
                }
                data.append(content)
    return data


# In[2]:


# creates db session
def createSession():
    try:
        # creates DB session
        session = mysql.connect(user=userOf, password=passOf, 
                                host=Url, database=DataBase,
                                auth_plugin='mysql_native_password')
    # catches errors if the occur
    except mysql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: username or password is incorrect...")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist...")
        else:
            print(err)
    return session


# In[3]:


# Adds data to the database
def AddDataToDB(query):
    # try/catch block to discover error and stop commits
    try:
        # creates DB session
        session = createSession()
        # opens dialog with DB
        cursor = session.cursor()
        # executes query
        cursor.execute(query);
        # closes dialog
        cursor.close()
    # catches errors if the occur
    except mysql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: username or password is incorrect...")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist...")
        else:
            print(err)
    else:
        # commits dialog to DB
        session.commit()
        # ends session
        session.close()
    
# Gets beer data
def Beer_Data_To_DB():
    content_data = data_combo()
    # makes db query
    for row in content_data:
        beer_name = row['name']
        beer_brew = row['brewery']
        beer_type = row['style']
        beer_perc = row['proof']
        beer_rate = row['rating']
        # action
        action_Q = ("INSERT INTO theCraftMapsCO_beer_table(Beer_Name, Beer_Brewery, Beer_Type, Beer_Percent, Beer_Rating)"+
            "VALUES('"+ beer_name +"', '"+ beer_brew +"', '"+ beer_type +"', "+ beer_perc +", "+ beer_rate +")")
        # adds data
        AddDataToDB(action_Q)  
    # finish
    return "Done..."


# In[5]:


# test
#data = data_combo()
#len(data)
#for d in data:
#    if d['brewery'] == "Brú Brewery":
#        print(d)

# enters data to db
Beer_Data_To_DB()


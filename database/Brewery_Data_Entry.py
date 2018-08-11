
# coding: utf-8

# In[6]:


import sys,re,ast,decimal
import mysql.connector as mysql
from mysql.connector import errorcode
from mysql.connector import (connection)
from decimal import Decimal

userOf = "UserOne"
passOf = "PassOne123#"
Url = "localhost"
DataBase = "CraftMapsDB"

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


# In[7]:


# Get row count
def getTableCount(tableName):
    # try/catch block to discover error and stop commits
    try:
        session = createSession()
        # query
        query = "SELECT COUNT(*) FROM %s" %tableName
        # opens dialog with DB
        cursor = session.cursor()
        # executes query
        cursor.execute(query);
        row_count = cursor.fetchone()
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
        # finish marker
        return row_count[0]
    
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
    
# Gets brewery data from text file
def BreweryDataToDB():
    fname = "new_database.txt"
    UD = []
    content_data = []
    with open(fname) as f:
        #reads all lines
        for content in f.readlines():
            content = re.sub("[a-zA-Z]['][a-zA-Z]","",content)
            content = re.sub('"',"'",content)
            data = eval(content)
            content_data.append(data)
    # adds data to DB
    guard_counter = 0
    DB_Count = (getTableCount('theCraftMapsCO_brewery_table'))
    for row in content_data:
        # redundent entries
        guard_counter = guard_counter+1
        if guard_counter > DB_Count:
            # creates query (Note: data has auto_increment for ID)
            b_name = str(row['name']).strip("(),'")
            b_region =str(row['region']).strip("(),'")
            b_type = str(row['type']).strip("(),'")
            rating=float(2.5)
            surl=str(row['url'])
            fabk=str(row['facebook'])
            twtt= str(row['twitter']).strip("(),'")
            tour=str(row['tour'])
            merch=str(row['merch'])
            adrs = str(row['address']).strip()
            adrs = re.sub(",","",adrs)
            adrs = re.sub("\s+"," ",adrs)
            adrs = re.sub("-"," ",adrs)
            
            
            lng=row['long']
            lat=row['lati']
            
            # enforce unique data
            counter = 0
            while lat in UD:
                counter = counter + 1
                if counter%2==0:
                    lat = lat + 0.0001
                    lng = lng - 0.001
                elif counter%10==0:
                    lat = lat - 0.001
                    lng = lng + 0.001
                else:
                    lat = lat - 0.001
                    lng = lng + 0.0001
                
            UD.append(lat)
            
            if lng > 0.0:
                lng = float(lng) * float(-1.0)
            if lat < 1.0:
                lat = float(lat) * float(1.0)
                
            action_Q = ("INSERT INTO theCraftMapsCO_brewery_table"+
            "(Brewery_Name, Brewery_Region, Brewery_Address, Brewery_Type, Brewery_Latitude, "
            "Brewery_Longitude, Brewery_Rating, Brewery_URL, Brewery_Twitter, Brewery_Facebook, Brewery_Tours, Brewery_Merch) "
            "VALUES('"+b_name+"', '"+b_region+"', '"+ adrs +"', '"+b_type
            +"', "+str(lat)
                        +", "+str(lng)+", "+str(rating)+", '"+surl+"', '"+twtt+"', '"+fabk+"', "+tour+", "+merch+")")

            # adds data
            AddDataToDB(action_Q)
    # finish marker
    return "Done..."


# In[8]:


BreweryDataToDB()


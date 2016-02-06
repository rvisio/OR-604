# -*- coding: utf-8 -*-
# 1) Go to http://www.menuism.com/restaurant-locations and navigate to the Domino’s Pizza Locations.
# Write a Python script that does the following:
# - Scrapes menuism and gathers the following information for each Domino’s store in the United States: state, city, store number, and URL (Hint: use beautifulSoup and REGEX)
# - Creates a database that will hold the information you scraped
#  - Loads the information into a database '''

from bs4 import BeautifulSoup
import requests
import sqlite3
import re
import math

"""1) Go to http://www.menuism.com/restaurant-locations and navigate to the Domino’s Pizza Locations.
Write a Python script that does the following:
    Scrapes menuism and gathers the following information for each Domino’s store in the United States: state, city, store number, and URL (Hint:  use beautifulSoup and REGEX)
    Creates a database that will hold the information you scraped
    Loads the information into a database
"""
def questionOne():
    #Deal with DB stuff
    dbName = 'dominos.db'
    myConnection = sqlite3.connect(dbName)
    myCursor = myConnection.cursor()
    # delete the dominos table if it already exists
    deleteSQL = """ DROP TABLE IF EXISTS dominos """
    myCursor.execute(deleteSQL)
    myConnection.commit()
    myCursor.close()
    #create dominos table
    myCursor = myConnection.cursor()
    createTableSQL = """ CREATE TABLE IF NOT EXISTS dominos
    (url text,
    storeNumber text,
    city text,
    state text); """
    myCursor.execute(createTableSQL)
    myConnection.commit()
    myCursor.close()

    # # Root dominos link to parse through
    rootUrl = 'http://www.menuism.com/restaurant-locations/dominos-pizza-7144'
    myPage = requests.get(rootUrl)
    soup = BeautifulSoup(myPage.content)
    # Get state urls from the root URL
    # Store in stateURL List
    stateUrl = []
    stateUrlList = soup.select('.popular-cities-box li a')
    counter = 0
    for tags in stateUrlList:
        if counter == 51:
            break
        stateUrl.append(tags['href'])
        counter += 1
    # Iterate through state URLS
    # Iterate through stores in each state
    currentState = ""
    soupyState = ""
    storeUrlList = []
    storeNumber = 0
    tempList = []
    list = []
    # iterate through each state URL
    for state in stateUrl:
        currentState = requests.get(state)
        soupyState = BeautifulSoup(currentState.content)
        storeUrlList = soupyState.select('ul.list-unstyled-links a') # get all store links on the state URL page

        # Iterate through each store link
        for store in storeUrlList:
            # get store number from URL
            storeNumber = re.search(r'(?<=-)\d{1,8}', str(store))
            print store
            try:
                storeNumber = storeNumber.group()
                #print ("Store number is " + storeNumber)
            except:
                print("Store number not acquired for store " + str(store))
                pass

            # get City and Stat from URL
            storeCityState = re.search(r'(?<=in\s)\D*(?=-)', str(store))
            try:
                cityState = storeCityState.group()
                city = cityState.rsplit(',',1)[0]
                #print("City is " + city)
                state = cityState.rsplit(',',1)[1]
                state = state.strip()
                #print('State is ' + state)

            except:
                print("-------------Something went wrong obtaining City and State")
                pass

            # get URL
            storeURL = store['href']
            print "For Store URL " + storeURL
            print "Store number is " + storeNumber
            print "City is equal to " + city
            print "State is equal to " + state

            #Insert values into database
            tempList.append((storeURL,storeNumber,city,state))

            print len(tempList)
            # Check if templist divisible by 5000
            if len(tempList) % 5000 == 0:
                myCursor = myConnection.cursor()
                print 'len of templist is divisble by 5000'
                myCursor = myConnection.cursor()
                myCursor.executemany('INSERT INTO dominos VALUES(?,?,?,?);',list)
                tempList =[]
                myConnection.commit()
                myCursor.close()

    #final check on templist insert stragglers
    if len(tempList) > 0:
        myCursor = myConnection.cursor()
        print 'finished looping still some left in tempList to insert into database'
        myCursor.executemany('INSERT INTO dominos VALUES(?,?,?,?);',tempList)
        tempList=[]
        myConnection.commit()
        myCursor.close()

"""2) Use the results of your McDonald’s homework from Lesson 01 (the one that you find all McDonald’s within 100 miles of each McDonald’s in New York)
to complete the following tasks in a Python Script:
    Select any 10 McDonald’s in New York and the associated stores that are within 100 miles of them
    Determine route distance (in KM) for each pair of those McDonald’s (hint use google maps distance matrix)
Save the following results in a datatable:  the two stores, each stores lat and lon, the haversine distance between the
two stores, and the route distance between the two stores """
#questionOne()
def questionTwo():
    # connect to mcdonalds database
    dbName = 'mcD.db'
    myConnection = sqlite3.connect(dbName)
    myCursor = myConnection.cursor()

    # Select ten random mcdonalds in state of NY
    # Create new table randomStores based off this query
    randomStoresSQL = """ CREATE TABLE randomStores AS
                      SELECT * FROM stores WHERE state == 'NY' ORDER BY RANDOM() LIMIT 10;"""
    myCursor.execute(randomStoresSQL)
    myConnection.commit()
    myCursor.close()

    # Dr C Code to







# haversine function calculates distance between two coordinate points
def haversine(lon1,lat1, lon2, lat2):

    lon1,lat1,lon2,lat2= map(radians, [lon1,lat1,lon2,lat2])

    dlon = lon2-lon1
    dlat = lat2-lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956
    return c *r


questionTwo()



















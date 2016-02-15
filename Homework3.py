# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from math import *
import requests, sqlite3,re
import json, urllib, time


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
    state text,
    lat FLOAT,
    lon FLOAT); """
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
    currentStore = ""
    storeCoord = ""
    latReg = ''
    storeLat = ""
    lngReg = ''
    storeLng = ''


    soupyStore = ""
    # iterate through each state URL
    for state in stateUrl:
        currentState = requests.get(state)
        soupyState = BeautifulSoup(currentState.content)
        storeUrlList = soupyState.select('ul.list-unstyled-links a') # get all store links on the state URL page

        # Iterate through each store link
        for store in storeUrlList:
            # get store number from URL
            storeNumber = re.search(r'(?<=-)\d{1,8}', str(store))
            #print store
            try:
                storeNumber = storeNumber.group()
                #print ("Store number is " + storeNumber)
            except:
                print("Store number not acquired for store " + str(store))
                pass

            # get City and Stat from URL
            storeCityState = re.search(r'(?<=in\s)\D*(?=-)', str(store))
            #print store

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
            currentStore = requests.get(storeURL)
            coordPage = SoupStrainer('div', class_='map-avatar')
            soupyStore = BeautifulSoup(currentStore.content, "lxml", parse_only=coordPage,) # Stack Overflow said lxml parser would speed up performance

            #storeCoord = soupyStore.find_all('div',class_='map-avatar', attrs={'data-bg'})
            storeCoord = soupyStore.find_all(coordPage)

            # regex to get lat (?<=lat=)\d*.\d*
            # regex to get lon (?<=lng=).\d*.\d*
            latReg = re.search(r'(?<=lat=)\d*.\d*', str(storeCoord))

            # Some issues with pages not having lat/lng, need to perform error handling
            try:
                storeLat = latReg.group()
                #print storeLat
                if storeLat.__contains__('&'):
                    storeLat = 0.0
            except:
                print 'error getting lat'
                pass
            lngReg = re.search(r'(?<=lng=).\d*.\d*', str(storeCoord))
            try:
                storeLng = lngReg.group()
               # print storeLng
                if storeLng.__contains__('&'):
                    storeLng = 0.0
            except:
             #   print 'error getting lng'
                pass

            #print(soupyStore.prettify())


            #Insert values into database
            tempList.append((storeURL,storeNumber,city,state,storeLat,storeLng))

            # Check if templist divisible by 5000
            print(len(tempList))
            if len(tempList) % 5000 == 0:
                myCursor = myConnection.cursor()
                #print 'len of templist is divisble by 5000'
                myCursor = myConnection.cursor()
                myCursor.executemany('INSERT INTO dominos VALUES(?,?,?,?,?,?);',tempList)
                tempList =[]
                myConnection.commit()
                myCursor.close()

    #final check on templist insert stragglers
    if len(tempList) > 0:
        myCursor = myConnection.cursor()
        #print 'finished looping still some left in tempList to insert into database'
        myCursor.executemany('INSERT INTO dominos VALUES(?,?,?,?,?,?);',tempList)
        tempList=[]
        myConnection.commit()
        myCursor.close()
questionOne()
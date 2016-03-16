# -*- coding: utf-8 -*-
# 1) Go to http://www.menuism.com/restaurant-locations and navigate to the Domino’s Pizza Locations.
# Write a Python script that does the following:
# - Scrapes menuism and gathers the following information for each Domino’s store in the United States: state, city, store number, and URL (Hint: use beautifulSoup and REGEX)
# - Creates a database that will hold the information you scraped
#  - Loads the information into a database '''

from bs4 import BeautifulSoup
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
            #print store
            try:
                storeNumber = storeNumber.group()
                #print ("Store number is " + storeNumber)
            except:
                print("Store number not acquired for store " + str(store))
                pass

            # get City and Stat from URL
            print storeCityState
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
            #print "For Store URL " + storeURL
            #print "Store number is " + storeNumber
            #print "City is equal to " + city
            #print "State is equal to " + state

            #Insert values into database
            tempList.append((storeURL,storeNumber,city,state))

            #print len(tempList)
            # Check if templist divisible by 5000
            if len(tempList) % 5000 == 0:
                myCursor = myConnection.cursor()
                #print 'len of templist is divisble by 5000'
                myCursor = myConnection.cursor()
                myCursor.executemany('INSERT INTO dominos VALUES(?,?,?,?);',tempList)
                tempList =[]
                myConnection.commit()
                myCursor.close()

    #final check on templist insert stragglers
    if len(tempList) > 0:
        myCursor = myConnection.cursor()
        #print 'finished looping still some left in tempList to insert into database'
        myCursor.executemany('INSERT INTO dominos VALUES(?,?,?,?);',tempList)
        tempList=[]
        myConnection.commit()
        myCursor.close()
questionOne()

"""2) Use the results of your McDonald’s homework from Lesson 01 (the one that you find all McDonald’s within 100 miles of each McDonald’s in New York)
to complete the following tasks in a Python Script:
    Select any 10 McDonald’s in New York and the associated stores that are within 100 miles of them
    Determine route distance (in KM) for each pair of those McDonald’s (hint use google maps distance matrix)
Save the following results in a datatable:  the two stores, each stores lat and lon, the haversine distance between the
two stores, and the route distance between the two stores """
def questionTwo():
    # connect to mcdonalds database
    dbName = 'mcD.db'
    myConnection = sqlite3.connect(dbName)
    myCursor = myConnection.cursor()

    # Drop randomStores table if it already exists
    deleteSQL = """ DROP TABLE IF EXISTS randomStores """
    myCursor.execute(deleteSQL)
    myConnection.commit()
    myCursor.close()
    # Select ten random mcdonalds in state of NY
    # Create new table randomStores based off this query
    myCursor = myConnection.cursor()

    randomStoresSQL = """ CREATE TABLE randomStores AS
                      SELECT * FROM stores WHERE state == 'NY' ORDER BY RANDOM() LIMIT 10;"""
    myCursor.execute(randomStoresSQL)
    myConnection.commit()
    myCursor.close()

    # Dr C Code to choose stores within 100 miles
    # Changed table to randomStores (10 random new york stores)
    # Will store all stores within 100 miles in tempDist, then insert into tblDistance
    myCursor = myConnection.cursor()
    sqlString = """
            SELECT tbl1.storeNumber, tbl1.lat, tbl1.lon, tbl2.storeNumber, tbl2.lat, tbl2.lon
            FROM randomStores as tbl1, stores as tbl2
            WHERE tbl1.state = 'NY'
            AND tbl2.lat <= tbl1.lat + 1.5
            AND tbl2.lat >= tbl1.lat - 1.5
            AND tbl2.lon <= tbl1.lon + 2.5
            AND tbl2.lon >= tbl1.lon - 2.5
            """
    myCursor.execute(sqlString)
    myData = myCursor.fetchall()
    # find stores exactly within 100 Miles and write them into the database tblDistance
    tempDist = []
    for n, row in enumerate(myData):
        distance = haversine(row[2], row[1], row[5], row[4])
        if distance <=100:
            tempDist.append((row[0],row[1],row[2], row[3],row[4],row[5], distance))


     # Drop randomStores table if it already exists
    myCursor = myConnection.cursor()

    # Drop tblDistance if already exists
    deleteSQL = """ DROP TABLE IF EXISTS tblDistance """
    myCursor.execute(deleteSQL)
    myConnection.commit()
    sqlString = """
                CREATE TABLE IF NOT EXISTS tblDistance
                (FromStore  INT,
                fromLat FLOAT,
                fromLon FLOAT,
                ToStore INT,
                toLat FLOAT,
                toLon FLOAT,
                Distance FLOAT)
                """
    myCursor.execute(sqlString)
    myConnection.commit()

    # Insert
    sqlStringInsert = "INSERT INTO tblDistance VALUES (?,?,?,?,?,?,?)"
    myCursor.executemany(sqlStringInsert, tempDist)
    myConnection.commit()
    tempDist = []



    # Select 250 random stores to calculate distnace from original (ten random stores) coordinates to destination
    # (25 of 250 stores)

    # Select 250 random stores in NY

##    getNYStores = """ SELECT * from tblDistance ORDER BY RANDOM() LIMIT 250;"""
##    myCursor.execute(getNYStores)
##    randomStoreList = [] # list of random ny stores
##    while True:
##        rows = myCursor.fetchall()
##        if not rows:
##            break
##        else:
##            for store in rows:
##                randomStoreList.append(store) # lat/lon and store number

#Save the following results in a datatable:  the two stores, each stores lat and lon, the haversine distance between the
#two stores, and the route distance between the two stores """
    # Drop FinalTable if already exists

    print('create final table')
    deleteSQL = """ DROP TABLE IF EXISTS FinalTable """
    myCursor.execute(deleteSQL)
    myConnection.commit()
    sqlString = """
                CREATE TABLE IF NOT EXISTS FinalTable
                (FromStore  INT,
                fromLat FLOAT,
                fromLon FLOAT,
                ToStore INT,
                toLat FLOAT,
                toLon FLOAT,
                HDistance FLOAT,
                GDistance FLOAT)
                """
    myCursor.execute(sqlString)
    myConnection.commit()

    finalTableList = []
    tempList =[]
    insertList = []
    count = 0
    # for randomStore in randomStoreList:
    #     tempList = []
    #     insertList = []
    #     for i in randomStore:
    #         tempList.append(i)
    #
    #     time.sleep(.1)
    #     gDistance = googleDistance(randomStore[1],randomStore[2],randomStore[4],randomStore[5])
    #
    #     tempList.append(gDistance)
    #     insertList.append(tuple(tempList))
    #     print insertList
    #     tempList.append(tuple(finalTableList))
    #     print tempList
    #     print count
    #     count += 1
    #     FinalTableSQL = """ INSERT INTO FinalTable VALUES(?,?,?,?,?,?,?,?); """
    #     myCursor.executemany(FinalTableSQL, insertList)
    #     myConnection.commit()



    #-------------------------------------------------------------
    #Was trying to do iterate through each storeNumber and pass that to the SQL Statement
    #Kept getting 'passing incorrect type' error or would run infinitely when passing tuple

    myCursor = myConnection.cursor()
    getNYStores = """ SELECT storeNumber from randomStores;"""
    myCursor.execute(getNYStores)
    randomStoreList = [] # list of random ny stores
    while True:
        rows = myCursor.fetchall()
        if not rows:
            break
        else:
            for store in rows:
                print store
                randomStoreList.append(store[0]) # lat/lon and store number
    randomNearByList = []
    for storeNum in randomStoreList:
        print storeNum

        x = str(storeNum)
        getRandomNearByStoreSQL = """SELECT * FROM tblDistance WHERE FromStore == (?) ORDER BY RANDOM() LIMIT 25;"""

        storeNum = (storeNum)
        myCursor.execute(getRandomNearByStoreSQL, (x,))
        while True:
            rows = myCursor.fetchall()

            if not rows:
                print('here')
                break
            else:
                for store in rows:
                    print('for loop')
                    print(store)
                    randomNearByList.append(store)

    # for item in randomNearByList:
    #     print ('randomNearByList')
    #     print item
    finalTableList = []
    tempList =[]
    insertList = []
    count = 0

    print(len(randomNearByList))
    for randomStore in randomNearByList:
        tempList = []
        insertList = []

        for i in randomStore:
            tempList.append(i)
        time.sleep(.1)

        print(randomStore[1],randomStore[2],randomStore[4],randomStore[5])

        gDistance = googleDistance(randomStore[1],randomStore[2],randomStore[4],randomStore[5])


        tempList.append(gDistance)
        insertList.append(tuple(tempList))
        tempList.append(tuple(finalTableList))
        print count
        count += 1
        FinalTableSQL = """ INSERT INTO FinalTable VALUES(?,?,?,?,?,?,?,?); """
        myCursor.executemany(FinalTableSQL, insertList)
        myConnection.commit()


def googleDistance(lat1,lon1,lat2,lon2):
    orig_coord = str(lat1)+','+str(lon1)
    dest_coord = str(lat2)+','+str(lon2)


    url = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s'\
          '&destinations=%s&mode=driving&language=en-EN&sensor=false'\
           % (str(orig_coord), str(dest_coord))
    result= json.load(urllib.urlopen(url))
    print result
    driving_time = 0.0
    driving_time = result['rows'][0]['elements'][0]["distance"]['value']
    return str(int(driving_time) / 1000.0)


def haversine(lat1,lon1,lat2,lon2):

    lon1,lat1,lon2,lat2= map(radians, [lon1,lat1,lon2,lat2])

    dlon = lon2-lon1
    dlat = lat2-lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956
    return c *r

questionTwo()







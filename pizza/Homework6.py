import csv, sqlite3
from math import *
from operator import itemgetter

#Set up sqlite db
dbName = 'hw_four.db'
myConnection = sqlite3.connect(dbName)
myCursor = myConnection.cursor()

# Haversine function to determine travel time
#TODO
# Should really be using google maps api -- will switch after testing with haversine
# Switch to google maps and store result in database so we don't need to call over and over
def haversine(lat1,lon1,lat2,lon2):

    lon1,lat1,lon2,lat2= map(radians, [lon1,lat1,lon2,lat2])

    dlon = lon2-lon1
    dlat = lat2-lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956
    return c *r


# Using answer from hw4 select all stores that have dc 5 has distribution center
answerSQL = "SELECT * FROM Answer"
myCursor.execute(answerSQL)
dcStoreList = []
while True:
        rows = myCursor.fetchall()
        if not rows:
            break
        else:
            for store in rows:
                if store[0] == '5':
                    dcStoreList.append(store[1])  # append store number


#Only using distribution center 5
myFile = open(r'dist.csv', 'rt')
myReader = csv.reader(myFile)
# get dc 5 and store in dc var
# dc type will be list
dc = ""
for row in myReader:
    if row[0] =='5':
        dc = row
        break
dcLat = float(dc[2])
dcLon = float(dc[3])

# Add store number and coordinates to storeLoc dictionary
storeLoc = {}
tempVal = ()
storeSQL = """SELECT * FROM stores WHERE storeNumber == (?)"""
for curStore in dcStoreList:
    val =  str(curStore)
    myCursor.execute(storeSQL, (val,))
    while True:
        rows = myCursor.fetchall()
        if not rows:
            break
        else:
            for x in rows:
                storeLoc[curStore] = (float(x[6]),float(x[7]))

# Dictionary of distance from dc 5 to store
# also add in bearing
bearing = 0.0
y = 0.0
x = 0.0
doughDemand = 0.0
storeBearing = []

demandSQL = """SELECT * FROM avgStoreDemand WHERE storeNumber == (?)"""
storeCoordDict = {}
for i in storeLoc:
    #TODO
    # Update haversine distance to google maps api
    hDistance = haversine(dcLat, dcLon, storeLoc[i][0],storeLoc[i][1])
    storeCoordDict[i] = storeLoc[i][0],storeLoc[i][1]
    #Calculate  bearing
    y = sin(storeLoc[i][1]-dcLon)* cos(storeLoc[i][0])
    x = cos(dcLat)*sin(storeLoc[i][0]) - sin(dcLat)*cos(storeLoc[i][0])*cos(storeLoc[i][1]-dcLon)
    bearing = atan2(y,x)

    curStore = str(i)
    myCursor.execute(demandSQL, (curStore,))

    # Pull the weekly demand from the avgStoreDemand database
    while True:
        rows = myCursor.fetchall()
        if not rows:
            break
        else:
            for x in rows:
                doughDemand =  float(x[2])

    #TODO
    # Determine number of product palletes
    # Lets just assume product pallets is 1/2 of dough pallets

    doughPallets = ceil(doughDemand/180)
    productPallets = ceil(doughPallets * 2)
    tempList = [int(i), bearing, hDistance, int(productPallets),int(doughPallets)]
    storeBearing.append(tempList)

# Sort list based on bearing
storeBearing = sorted(storeBearing, key=itemgetter(1))



# Dough needed will be determined from avgStoreDemand
# 85% of supply normal dough 15% of za is crispy thin crust
# 1.5 cup sauce per pizza
# 2.25 cups of cheese


# create capacity dictionary -- based off of capacity of each truck
# Produce = key, value = dough
capacity = {44:0,43:0,42:0,41:1,40:1,39:2,38:2,37:3,36:3,35:3,34:4,
            33:4,32:5,31:5,30:6,29:6,28:7,27:7,26:8,25:8,24:9,
            23:9,22:10,21:10,20:10,19:11,18:11,17:12,16:12,15:13,
            14:13,13:14,12:14,11:14,10:15,9:15,8:16,7:16,6:17,
            5:17,4:18,3:18,2:19,1:19,0:20}

# Begin Routing Heuristic

# ALL TIMES IN MINUTES
# ALL DISTANCE IN MILES
# ALL ZA IN DOMINOS
numTrucks = 1
truckLocation = "DistCenter"
truckTime = 0
#product, dough
truckCapacity = [0,0]
truckRoute = {}
serviceTime = 45

for store in storeBearing:
    AddStore = False
    newProductTotal = truckCapacity[0] + store[3]    # total pallete of current truck capacity and store required
    # Check truck capacity against current capacity
    try:
        if capacity[newProductTotal] > truckCapacity[1]:
            #TODO
            # Update haversine to GOOGLE API
            # Currently assuming distance in miles divided by 55 mph (max speed for truckers)
            curStoreStr = str(store[0])
            print curStoreStr
            curStoreLat = storeCoordDict[curStoreStr][0]
            curStoreLon = storeCoordDict[curStoreStr][1]

            # Time from current store back to distribution center
            timeBackToDC = (haversine(dcLat,dcLon,curStoreLat,curStoreLon))/55

            if timeBackToDC+truckTime+serviceTime < 14*60:    # If we can get back to store and not be over 14 hours
                 # add store to route this truck is taking
                truckRoute.append(store)
                 # add values to truckCapacity
                truckCapacity[0] += store[3]
                truckCapacity[1] += store[4]
                # add time to truckTime
                truckTime += serviceTime+(store[2]/55)+serviceTime
                truckLocation = store[0]
                AddStore = True
    except:
        if AddStore != True:  # truck needs to head back to depot, this route is complete
            print 'uh oh'
            #TODO
            # Record truck route
            # Update truck route to dc -> cur store
            # TruckLocation = next store
            # Truck capacity = next store product, dough
            # update trucktime
            numTrucks += 1
















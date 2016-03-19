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

# create capacity dictionary -- based off of capacity of each truck
# Produce = key, value = dough
capacity = {44:0,41:1,39:2,37:3,34:4,
            32:5,30:6,28:7,26:8,24:9,
            22:10,19:11,17:12,15:13,
            13:14,10:15,8:16,6:17,
            4:18,2:19,0:20}

# Dictionary of distance from dc 5 to store
# also add in bearing
bearing = 0.0
y = 0.0
x = 0.0
doughDemand = 0.0
storeBearing = []

demandSQL = """SELECT * FROM avgStoreDemand WHERE storeNumber == (?)"""
for i in storeLoc:
    #TODO
    # Update haversine distance to google maps api
    hDistance = haversine(dcLat, dcLon, storeLoc[i][0],storeLoc[i][1])

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

    doughPallets = ceil(doughDemand/180.0)
    tempList = [int(i), bearing, hDistance, doughPallets]
    storeBearing.append(tempList)

# Sort list based on bearing
storeBearing = sorted(storeBearing, key=itemgetter(1))


for i in storeBearing:
    print i
# Dough needed will be determined from avgStoreDemand
# 85% of supply normal dough 15% of za is crispy thin crust
# 1.5 cup sauce per pizza
# 2.25 cups of cheese

# One dough pallete = 180 doughs
# product pallete can store 12 cheese units, 10 sauce units, or 6 thin crust per tray
# lets assume 8 trays per product pallete














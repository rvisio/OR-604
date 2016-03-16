import csv,sqlite3
from math import *

dbName = 'hw_four.db'
myConnection = sqlite3.connect(dbName)
myCursor = myConnection.cursor()

# Haversine function to determine travel time
# Should really be using google maps api -- will switch after testing with haversine
# Google maps api has call limit
def haversine(lat1,lon1,lat2,lon2):

    lon1,lat1,lon2,lat2= map(radians, [lon1,lat1,lon2,lat2])

    dlon = lon2-lon1
    dlat = lat2-lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956
    return c *r

# Using previous answer select all stores that have dc 5 has distribution center
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
                    dcStoreList.append(store[1]) # append store number


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
distToStore = {}
bearing = 0.0
y = 0.0
x = 0.0
for i in storeLoc:
    hDistance = haversine(dcLat, dcLon, storeLoc[i][0],storeLoc[i][1])
    y = sin(storeLoc[i][1]-dcLon)* cos(storeLoc[i][0])
    x = cos(dcLat)*sin(storeLoc[i][0]) - sin(dcLat)*cos(storeLoc[i][0])*cos(storeLoc[i][1]-dcLon)
    bearing = atan2(y,x)
    distToStore[int(i)] = (hDistance, bearing)


for i in distToStore:
    print i, distToStore[i]






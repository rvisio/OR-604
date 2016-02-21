# -*- coding: utf-8 -*-
import csv, sqlite3, timeit
from gurobipy import *
from math import *

# Set up db stuff
dbName = 'hw_four.db'
myConnection = sqlite3.connect(dbName)
myCursor = myConnection.cursor()


# Haversine function
def haversine(lat1,lon1,lat2,lon2):

    lon1,lat1,lon2,lat2= map(radians, [lon1,lat1,lon2,lat2])

    dlon = lon2-lon1
    dlat = lat2-lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956
    return c *r



# Create good dominos sql table
createTableSQL = """ CREATE TABLE IF NOT EXISTS storeDemand
                     (storeNumber integer,
                     demand FLOAT); """
myCursor.execute(createTableSQL)
myConnection.commit()


dropStoresSQL = """DROP TABLE IF EXISTS stores"""
myCursor.execute(dropStoresSQL)
myConnection.commit()
#create stores table
myCursor = myConnection.cursor()
createTableSQL = """ CREATE TABLE IF NOT EXISTS stores
    (storeNumber text,
    store text,
    street text,
    city text,
    state text,
    zip text,
    lat FLOAT,
    lon FLOAT); """
myCursor.execute(createTableSQL)
myConnection.commit()

# Load the Dominos stores into the stores dictionary
stores = {}
tempList = []
myFile = open(r'OR604 Good Dominos Data.csv', 'rt')
myReader = csv.reader(myFile)
counter = 0 # created to skip reading headers
for row in myReader:
    if counter == 0:
        counter += 1
        continue
    #storeNumber      #address      #state      #zip             #lat           #long
    stores[row[0]] = (str(row[2]), str(row[3]), str(row[4]), float(row[5]), float(row[6]))

    tempList.append(tuple(row))
    if len(tempList)%5000 ==0:
        myCursor.executemany('INSERT INTO stores VALUES(?,?,?,?,?,?,?);',tempList)
        myConnection.commit()
        tempList =[]
if len(tempList) > 0:
    myCursor.executemany('INSERT INTO stores VALUES(?,?,?,?,?,?,?,?);',tempList)
    myConnection.commit()
    tempList =[]
myFile.close

#Insert Scores into database
# demand = {}
# tempList = []
# tempRow = []
# myFile = open(r'OR 604 Dominos Daily Demand.csv', 'rt')
# myReader = csv.reader(myFile)
# counter = 0 # created to skip headers
# #Insert store demand into store demand table
# for row in myReader:
#     if counter == 0:
#         counter += 1
#         continue
#     # storeNumber
#     tempRow = (row[1],row[2])
#     tempList.append(tuple(tempRow))
#     if len(tempList) % 5000 == 0:
#         myCursor.executemany('INSERT INTO storeDemand VALUES(?,?);',tempList)
#         tempList =[]
#         myConnection.commit()
#         tempRow = []
#
#     tempRow =[]
#
# if len(tempList) > 0 :
#     print('inserting remainder')
#     myCursor.executemany('INSERT INTO storeDemand VALUES(?,?);',tempList)
#     tempList =[]
#     myConnection.commit()
#     tempRow = []
# myFile.close
#
#
# createAvgTable = """ CREATE TABLE IF NOT EXISTS avgStoreDemand
#                     (storeNumber integer,
#                     demand FLOAT); """
# myCursor.execute(createAvgTable)
# myConnection.commit()

#start = timeit.default_timer()
#SLOW AF
#code to average
# print ('about to run avgStoreDemand')
#
# avgSQL = """  insert INTO avgStoreDemand
#                 SELECT storeNumber, AVG(demand)
#                 from storeDemand
#                 group by storeNumber;"""
# print ('about to run avgStoreDemand2')
#
# stop = timeit.default_timer()
# print ('about to run avgStoreDemand3')
#
# myCursor.execute(avgSQL)
# print ('about to run avgStoreDemand4')
#
# myConnection.commit()
# print ('about to run avgStoreDemand5')


# Using PANDAS to calculate average
# start = timeit.default_timer()
# data = pd.read_csv("OR 604 Dominos Daily Demand.csv", low_memory=False)
# stop = timeit.default_timer()
# print 'pandasTest.py took ' + str(stop - start) + ' seconds to read csv'
#
# start = timeit.default_timer()
# df = data.groupby(['Store Number']).mean()
# stop = timeit.default_timer()
# print 'pandasTest.py took ' + str(stop - start) + ' seconds to caclulate mean'


# Code to create weeklyDemand column (daily demand * 7)

#ALTER TABLE avgStoreDemand ADD COLUMN weeklyDemand FLOAT;
#update avgStoreDemand set weeklyDemand = ROUND(demand*7,2)

# print 'here'
# myCursor.execute("""SELECT * FROM avgStoreDemand""")
# myConnection.commit()

deleteDistCentersSQL = """ DROP TABLE IF EXISTS distCenters """
myCursor.execute(deleteDistCentersSQL)
myConnection.commit()

#Create table for distribution tables
createDistSQL = """ CREATE TABLE IF NOT EXISTS distCenters
                      (ID INTEGER,
                      address text,
                        lat FLOAT,
                        long FLOAT,
                        weeklyCapacity FLOAT,
                        dailyCapacity FLOAT,
                        CostPerMile FLOAT); """
myCursor.execute(createDistSQL)
myConnection.commit()

tempList = []
# Read in distribution centers
myFile = open('dist.csv','rt')
myReader = csv.reader(myFile)
counter = 0 # created to skip reading headers
for row in myReader:
    #print row
    if counter == 0:
        counter += 1
        continue

    tempList.append(tuple(row))

myCursor.executemany('INSERT INTO distCenters VALUES(?,?,?,?,?,?,?);',tempList)
myConnection.commit()



# Final Table for all store info
# #Store Number, Street, City, State, Zip Avg Daily Demand, Avg Weekly Demand, Distance from DC 1, 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
# totalStoreInfoSQL  = """CREATE TABLE IF NOT EXISTS totalStoreInfo
#                         (StoreNumber INTEGER,
#                         Street TEXT,
#                         City TEXT,
#                         State TEXT,
#                         Zip TEXT,
#                         lat FLOAT,
#                         long FLOAT,
#                         AvgDailyDemand FLOAT,
#                         AvgWeeklyDemand FLOAT,
#                         )"""
# myCursor.execute(totalStoreInfoSQL)
# myConnection.commit()

deleteSQL = """ DROP TABLE IF EXISTS distToStore """
myCursor.execute(deleteSQL)
myConnection.commit()

storeToDistSQL = """CREATE TABLE IF NOT EXISTS distToStore
                 (Dist INTEGER,
                 ToStore INTEGER,
                 Distance FLOAT,
                 CostOfTravel FLOAT)"""
myCursor.execute(storeToDistSQL)
myConnection.commit()

storesSQL = """SELECT * from stores"""
myCursor.execute(storesSQL)
storeInfo = myCursor.fetchall()

distSqlString = """SELECT * from distCenters"""
myCursor.execute(distSqlString)
distCenters = myCursor.fetchall()

#Iterate thtrough distCenters
distLat = 0.0
distLong = 0.0
curStoreLat = 0.0
curStoreLong = 0.0
distNumber = 0
currentStoreNumber = 0
hDistance = 0.0
tempList = []
tempRow = []
costOfTrip = 0.0
distCost = 0.0
for currentDist in distCenters:
    print currentDist
    distLat = float(currentDist[2])
    distLong = float(currentDist[3])
    distCost = float(currentDist[6])
    distNumber = currentDist[0]
    for currentStore in storeInfo:
        currentStoreNumber = currentStore[0]
        curStoreLat = float(currentStore[6])
        curStoreLong = float(currentStore[7])
        hDistance = haversine(curStoreLat,curStoreLong, distLat, distLong)
        #print 'haversine for dist center ' + str(distNumber) + ' to dominos store ' + str(currentStoreNumber) + ' is ' +  str(hDistance)
        costOfTrip = distCost * hDistance
        tempRow = (distNumber, currentStoreNumber, hDistance, costOfTrip)
        tempList.append(tuple(tempRow))

        tempRow =[]
        if len(tempList) % 5000 == 0:

            myCursor.executemany('INSERT INTO distToStore VALUES(?,?,?,?);',tempList)
            tempList =[]
            myConnection.commit()
            tempRow = []

    if len(tempList)> 0:
        myCursor.executemany('INSERT INTO distToStore VALUES(?,?,?,?);',tempList)
        tempList =[]
        myConnection.commit()
        tempRow = []


# It's Modeling Time
#--------------------------------------------------------
# Objective Function
# Minimize cost of dough sent from distribution center to individual store
# Calculating on weekly basis, one truck leaves distribution center and goes to store
#--------------------------------------------------------
# Constraints
# Stores receive minimum supply (weekly demand)
# Dist center does not ship more than weekly capacity
# Dough per truck less than 9.9K doughs? (12 doughs per tray, 25 trays per pallet, 33 pallets per truck)
#--------------------------------------------------------
# stores receive minimum supply of dough (minimum supply = demand)
#
# zaModel = Model()
# zaModel.modelSense = GRB.M






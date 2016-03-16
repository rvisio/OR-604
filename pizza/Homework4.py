# -*- coding: utf-8 -*-
import csv, sqlite3, timeit
from gurobipy import *
from math import *

# Set up db stuff
dbName = 'hw_four.db'
myConnection = sqlite3.connect(dbName)
myConnection.text_factory = str #fixes some bullshit unicode error that was messing up setting up constraints
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
#         print('inserting 5 k')
#         myCursor.executemany('INSERT INTO storeDemand VALUES(?,?);',tempList)
#         myConnection.commit()
#         tempList =[]
#         tempRow = []
#
#     tempRow =[]
#
# if len(tempList) > 0 :
#     print('inserting remainder')
#     myCursor.executemany('INSERT INTO storeDemand VALUES(?,?);',tempList)
#     myConnection.commit()
#     tempList =[]
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
# print ('about to run avgStoreDemand

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
                      (ID TEXT,
                      address text,
                        lat FLOAT,
                        long FLOAT,
                        weeklyCapacity INTEGER,
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
                 CostOfTravel FLOAT,
                 PricePerDough FLOAT)"""
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
pricePerDough = 0.0
for currentDist in distCenters:
    #print currentDist
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
        pricePerDough = costOfTrip / 9900
        tempRow = (distNumber, currentStoreNumber, hDistance, costOfTrip, pricePerDough)
        tempList.append(tuple(tempRow))

        tempRow =[]
        if len(tempList) % 5000 == 0:

            myCursor.executemany('INSERT INTO distToStore VALUES(?,?,ROUND(?,2),ROUND(?,2),?);',tempList)
            tempList =[]
            myConnection.commit()
            tempRow = []

    if len(tempList)> 0:
        myCursor.executemany('INSERT INTO distToStore VALUES(?,?,ROUND(?,2),ROUND(?,2),?);',tempList)
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

# Cost of shipping from dist i to store j
# variable = number of doughs
#-------------------------------------------------------------------------------------------------
#Indexes

#Distribution Center Index
tempDC = []
for i in distCenters:
    tempDC.append(i[0])
DC = tuple(tempDC)

#Store Number Index
tempStoreList = []
for i in storeInfo:
    tempStoreList.append(i[0])
storeList = tuple(tempStoreList)
#-------------------------------------------------------------------------------------------------

# CostPerDough Dictionary
storesSQL = """SELECT * from distToStore"""
myCursor.execute(storesSQL)
distInfo = myCursor.fetchall()

costPerDough = {}
for i in distInfo:
    costPerDough[i[0],i[1]] = (i[4])

# Minimum Demand Per Store
MinStoreDemand = {}
storesSQL = """SELECT * from avgStoreDemand"""
myCursor.execute(storesSQL)
avgStoreInfo = myCursor.fetchall()
for i in avgStoreInfo:
    MinStoreDemand[i[0]] = (i[2])

# Maximum Capacity Per Distribution Center
DCLimit = {}
for i in distCenters:
    #temp = i[4]
   # print temp

 #  # print temp
    #temp = temp.replace(',', '')
 #   print temp
    #temp = int(temp)
    #print temp
    #print '-------------'
    DCLimit[i[0]] = (int(i[4]))

# for i in DCLimit:
#     print '____________________'
#     print type(i)
#     print DCLimit[i]




#Create distance matrix dictionary
#populate it with values from distribution center to store database
# costMatrix = {}
# for current in distInfo:
#    #print current
#     costMatrix[current[0],current[1]] = (float(current[3]),float(current[4]))

zaModel = Model()
zaModel.modelSense = GRB.MINIMIZE
zaModel.update()

# Add in variables
# Our variable is number of doughs to ship to a store from a distribution center

dough = {}
for route in costPerDough:
    #print costPerDough[route]
    #print route
    #print costPerDough[route]*9900
    try:
        #print route[0]
        dough[route] = zaModel.addVar(obj= costPerDough[route],
                                  name = '%s_%s_dough' % (str(route[0]),str(route[1])))
        #dough[route] = zaModel.addVar(obj= cost)
        pass
    except KeyError:
        dough[route] = zaModel.addVar(obj=175*3,
                                      name = '%s_%s_dough' % (str(route[0]), str(route[1])))

zaModel.update()


#Adds in the cost of traveling from distribution center to store as
# Variable is the number of doughs shipped


# edgeCost = {}
# for dc,store in costMatrix:
#     edgeCost[dc,store] = zaModel.addVar(obj=costMatrix[dc,store][1],
#                                         name='cost_from_%s_to_%s' % (dc,store))
#
# zaModel.update()
#
# #Create constraints dictionary
constraints = {}
#
# # First Constraint is the capacity available in each distribution center
# # Pull capacity from distCenters table distCenter[4]
# # distCenter[4] must be <=
#
# # Create Distribution center Dictionary
distCentersConstrSQL = """SELECT * from distCenters"""
myCursor.execute(distCentersConstrSQL)
distConstr = myCursor.fetchall()
dist = {}
for center in distConstr:
    insertVar = center[4]
    #insertVar = insertVar.replace(',','')
    dist[center[0]] = (insertVar)
#
# print
# # Create Store Dictionary
# # storesSQL = """SELECT * from avgStoreDemand"""
# # myCursor.execute(storesSQL)
# # avgStoreInfo = myCursor.fetchall()
# # avgStoreDemand = {}
# # for store in avgStoreInfo:
# #     avgStoreDemand[store[0]] = (float(store[2])) #stores weekly demand as float
#
#
#
for center in dist:
    #print center
    constrName = '%s_Center_Supply' % center
    #print constrName

    limit = dist[center[0]]
    # print type(limit)
    #print limit
    limit = int(limit)
    # print '-0o0-4353453'
    # print limit
    # print limit
    # print type(limit)
   # print dist[center][0]

    constraints[constrName] = zaModel.addConstr((quicksum(dough[int(center), int(store)]
                                                         for store in MinStoreDemand)* 9900) * 3 <= limit,
                                                name = constrName)

zaModel.update()
#
# # Second Constraint is the demand created by each store
# # The supply sent to the store must match the weekly demand the store has
# # Weekly demand is pulled from avgStoreDemand[2]
#
for store in MinStoreDemand:
    #print avgStoreDemand[str(store)[0]]
    #print type(store)
    constrName = '%s_demand' % store
    # print store
    # print avgStoreDemand[store]

    minimumNeeded = int(MinStoreDemand[store])
    # print '--------------'
    # print minimumNeeded
    #minimumNeeded = minimumNeeded
    total = costPerDough[int(center),int(store)]
    #print minimumNeeded

    constraints[store] = zaModel.addConstr((quicksum(dough[int(center),int(store)]
                                                  for center in dist) * 9900)* 3 >= minimumNeeded,
                                         name = constrName)

zaModel.update()
zaModel.write('za.lp')
zaModel.optimize()

DROPTABLESQL = """DROP TABLE IF EXISTS Answer"""
myCursor.execute(DROPTABLESQL)
myConnection.commit()

SQLSTRING = """CREATE TABLE IF NOT EXISTS Answer (Dist TEXT, Store TEXT, EX TEXT)"""
myCursor.execute(SQLSTRING)
myConnection.commit()

tempDC = ""
tempStore = ""
tempList = []
if zaModel.Status == GRB.OPTIMAL:
    for e in dough:
        if dough[e].x > 0:

            print e, dough[e].x
            val = (str(e[0]),str(e[1]),str(dough[e].x))
            tempList.append(val)

myCursor.executemany('INSERT INTO Answer VALUES(?,?,?);',tempList)
myConnection.commit()









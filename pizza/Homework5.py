# -*- coding: utf-8 -*-
import sqlite3, csv
import pandas as pd
from gurobipy import *
from math import *

# Haversine function
def haversine(lat1,lon1,lat2,lon2):

    lon1,lat1,lon2,lat2= map(radians, [lon1,lat1,lon2,lat2])

    dlon = lon2-lon1
    dlat = lat2-lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956
    return c *r

#Problem 1
# Re-do homework 4 (assigning stores to dist centers)
# 3 days worth of demand ( stores getting supplied twice a week), cut dist center supply in half
# If a store is missing from the Demand data, give it avg value of 175
# Each store can only be supplied by a single dist center



# set up db
dbName = 'hw5.db'
myConnection = sqlite3.connect(dbName)
myCursor = myConnection.cursor()

# Read in csv with average store demand using Pandas
demandData = pd.read_csv("OR 604 Dominos Daily Demand.csv", low_memory=False)
demandData = demandData.drop('Date',1)
demandData = demandData.groupby(['Store Number'], as_index=False).mean()
#data = data.reset_index() This also works if you dont include as_index=False
demandData['ThreeDayDemand'] = demandData['Pizza Sales'].values * 3 # multiply daily demand by 3 to fulfill 3 day demand req
demandData['ThreeDayDemand'] = demandData['ThreeDayDemand'].round(2)

# Read in Dominos Store csv to see if store data is missing from df
storeData = pd.read_csv("OR604 Good Dominos Data.csv", low_memory=False)

# Check which stores are missing from our dataframe
missingStoreList = []
for i in storeData.itertuples():
    store = i[1]
    storeList = demandData['Store Number'].tolist()
    if store in storeList:
        pass
    else:
        missingStoreList.append(store)

# Insert missing stores to demandData frame with 175 daily and 3 day avg
for i in missingStoreList:
    demandData.loc[len(demandData)]=[i,175,175*3]

# Read in Distribution Centers
distDF = pd.read_csv("dist.csv", low_memory=False)

insertList = []
tempRow = []
distCenter = 0
storeNumber = 0
hDist = 0.0
# dist center lat /lng
dLat = 0.0
dLng = 0.0
# store lat/lng
sLat = 0.0
sLng =0.0
costOfTrip = 0.0
pricePerDough = 0.0
distCost = 0.0

# Create DC to Store Data Frame
for dc in distDF.itertuples():
    distCenter = dc[1]
    dLat = dc[3]
    dLng = dc[4]
    distCost = dc[7]
    for store in storeData.itertuples():
        storeNumber = store[1]
        sLat = store[7]
        sLng = store[8]
        hDist = haversine(dLat,dLng,sLat,sLng)
        costOfTrip = distCost * hDist
        pricePerDough = costOfTrip / 9900
        tempRow = (distCenter, storeNumber, hDist, costOfTrip, pricePerDough)
        insertList.append(tempRow)
distToStore = pd.DataFrame(insertList, columns= ["DistCenter", "StoreNumber","Distance","CostOfTrip", "PricePerDough"])



# It's Modeling Time
#-----------------------------
#Data Frames
# distToStore - from distribution center to store, contains DC, StoreNumber, Distance, Cost of Trip, PricePerDough
# distDF - distribution center data Frame
# storeData - information on stores data frame
# demandData - contains store demand data information Store Number sales and 3 day demand

# Indexes
# Distribution Centers
distCenters = {}
for i in distDF.itertuples():
    distCenters[i[1]] = int(i[5])

# Domino Stores
domStores = {}
for i in demandData.itertuples():
    domStores[i[1]] = int(i[3])

# Create Cost Matrix
costMatrix  = {}
print distToStore.head()
for i in distToStore.itertuples():
    costMatrix[i[1],i[2]] = float(i[5])

zaModel = Model()
zaModel.modelSense = GRB.MINIMIZE
zaModel.update()

dough = {}
for dist, store in costMatrix:
    dough[dist,store] = zaModel.addVar(vtype = GRB.BINARY,
                                       obj = costMatrix[dist,store] * domStores[store],
                                       name = 'Dough_%s_%s' % (dist,store))



myConstrs = {}

for

zaModel.update()

zaModel.write('za.lp')
zaModel.optimize()

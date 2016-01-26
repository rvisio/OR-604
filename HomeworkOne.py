# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 23:05:28 2016

@author: Rob
"""
import os
import sqlite3
import csv
import random
from math import * 
dbName = ''

def questionOne(a,b):
    if a%b==0:
        return True
    return False
    
def questionTwo(a,b,c):
    return max(a,b,c)
    
def questionThree(a,b):
    """
    binomial expansion one
    """

def questionFour(n,k):
    for i in range(0,k):
        print(random.randint(0,n))
    
def questionFive(a,b):
    return (str(a) +str(b))
    
def questionSix():
    print("Question one using values 4 and 2")
    print(questionOne(4,2))
    print("Question one using values 4 and 9")
    print(questionOne(4,9))

    print("Question two using values 500, 6, 10000")
    print(questionTwo(500,6,10000))
    
    print("Question Four using values 20,50")
    print(questionFour(20,50))
    
    print("Question five using values 500 and 10000")
    print(questionFive(500,10000))
    print("Question five using values 'Cheers' and 'Mate'")
    print(questionFive( 'Cheers','Mate'))
 
    
    
    
#questionSix()

def sqlQuestionOne():
    
    
    # gets path of python script and pulls mcdonalds csv from that directory
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file = os.path.join(__location__, 'mcDonalds.csv')
    
    # creates db, sets up cursor
    global dbName
    dbName = 'mcD.db'
    myConnection = sqlite3.connect(dbName)
    myCursor = myConnection.cursor()

    # delete the stores table if it already exists
    deleteSQL = """ DROP TABLE IF EXISTS stores """
    myCursor.execute(deleteSQL)
    myConnection.commit()
    myCursor.close()
    #create stores table
    myCursor = myConnection.cursor()
    createTableSQL = """ CREATE TABLE IF NOT EXISTS stores 
                         (name text,
                         address text,
                         city text,
                         state text,
                         zip integer,
                         lat numeric,
                         lon numeric,
                         storeNumber integer); """

    myCursor.execute(createTableSQL)    
    myConnection.commit()    
    
    # read the mcdonalds csv 
    myFile = open(__location__ + '\\mcDonalds.csv','rt')
    myReader = csv.reader(myFile)
    
    tempList = []
    iterator = 0
    # insert values into stores table
    for row in myReader:
        tempList.append(tuple(row))
        if len(tempList) % 5000 == 0:
            myCursor.executemany('INSERT INTO stores VALUES(?,?,?,?,?,?,?,?);',tempList)
            tempList =[]
            myConnection.commit()
    
    myCursor.executemany('INSERT INTO stores VALUES(?,?,?,?,?,?,?,?);',tempList)
    myConnection.commit()
    # clean up
    myCursor.close()
    myConnection.close()
    myFile.close()
    myReader = None
    

sqlQuestionOne()

def sqlQuestionTwo():
    dist = 0.0
    withinDistList = []
    lat = 0.0
    lon= 0.0
    lat2= 0.0
    lon2= 0.0 
     # sets database to db defined in sql question one, using python file directory
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    myDB = __location__ + "\\" + dbName
    myConnection = sqlite3.connect(myDB)
    myCursor = myConnection.cursor()
    
    # iterate through db to find min/max lat/lon for all mcdonalds in state of NY
    nyLatSQLString = """ SELECT lat,lon,storeNumber FROM stores WHERE state = 'NY' """
    myCursor.execute(nyLatSQLString)
    
    coordList = []
    # store lat/lon information from all mcdonalds in NY
    while True:
        rows = myCursor.fetchmany(5000)
        if not rows:
            break
        else:
            for store in rows:
                coordList.append([store[0],store[1],store[2]]) # lat/lon and store number
  
    myCursor.close()
    myCursor = myConnection.cursor()
    mcdSQLString = """ SELECT lat,lon, storeNumber FROM stores WHERE state != 'NY' """
    myCursor.execute(mcdSQLString)
    
    iterator = 0
    tempCoord = list()
    while True: 
        rows = myCursor.fetchmany(5000)
        if not rows:
            break
        else:
            for x in range(len(coordList)):
                tempCoord = coordList[x]
                lat = float(tempCoord[0])
                lon = float(tempCoord[1])
               # print str(tempCoord[0]) + " " + str(tempCoord[1]) + " " +  str(tempCoord[2])
                for y in rows:
                    lat2 = float(y[0])
                    lon2 = float(y[1]) 
                    #print str(y[0]) + str(y[1]) + " " + str(y[2])
                    dist = haversine(lon,lat,lon2,lat2)
                    print dist
                  
                   

                
                
       
    # use haversine formula to calculate lat/lon within 100 miels based on min/max lat/lon
    
    # create new table using values of mcdonalds in NY and mc donalds within 100 miles
    
    # cleanup
    
# haversine function calculates distance between two coordinate points
def haversine(lon1,lat1, lon2, lat2):
    
    lon1,lat1,lon2,lat2= map(radians, [lon1,lat1,lon2,lat2])
    
    dlon = lon2-lon1
    dlat = lat2-lat1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 
    return c *r
    

sqlQuestionTwo()


def sqlQuestionThree():
    pass
    #implemented in sqlQuestionOne
#    for row in myReader:
#        tempList.append(tuple(row))
#        if len(tempList) % 5000 == 0:
#            myCursor.executemany('INSERT INTO stores VALUES(?,?,?,?,?,?,?,?);',tempList)
#            tempList =[]
#            myConnection.commit()
#    
#    myCursor.executemany('INSERT INTO stores VALUES(?,?,?,?,?,?,?,?);',tempList)
#    myConnection.commit()
#    # clean up
#    myCursor.close()
#    myConnection.close()
#    myFile.close()
#    myReader = None

    
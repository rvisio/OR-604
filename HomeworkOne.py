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

#Create a simple function that takes two numbers and determines if the first number is evenly divisible by the second number.
#Your function should return a Boolean value that indicates the result
def questionOne(a,b):
    if a%b==0:
        return True
    return False

#Python 2:  Create function in Python that takes three numbers and determines which is the largest of the three.
#Your function should return the number
def questionTwo(a,b,c):
    return max(a,b,c)

#Python 3:  Create a function in Python that prints out the coefficients (in order) for all terms of the kth binomial expansion.
#Your function should accept as its argument the power by which the binomial is being expanded.
def questionThree(n):
   row = [1]
   k = [0]
   for x in range(n-1):
      row=[l+r for l,r in zip(row+k,k+row)]
   return row

# Import the random module.  Write a procedure that takes two arguments (the upper limit “n” of a range of numbers,
#and the number “k” of values to return) and returns “k” random elements from 0 to “n” without replacement.
def questionFour(n,k):
    #for #i in range(0,k):
    print random.sample(range(n),k)

#Create a function that takes any two values (numbers or strings) and concatenates them (look it up).
#Your function should return the concatenated string
def questionFive(a,b):
    return (str(a) +str(b))
    
def questionSix():
    print("Question one using values 4 and 2")
    print(questionOne(4,2))
    print("Question one using values 4 and 9")
    print(questionOne(4,9))

    print("Question two using values 500, 6, 10000")
    print(questionTwo(500,6,10000))

    print("Question three using values n=5")
    print(questionThree(5))

    print("Question Four using values n=50,k=50")
    print(questionFour(50,50))
    
    print("Question five using values 500 and 10000")
    print(questionFive(500,10000))
    print("Question five using values 'Cheers' and 'Mate'")
    print(questionFive( 'Cheers','Mate'))

    print("Python Question Six Completed")
 
    
    

questionSix()

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
    
    # delete header from csv in sqlite database, db is reading in header row and is affecting
    # haversine calculatino for sqlQuestionTwo
    deleteHeaderSQL = """ DELETE FROM stores WHERE name = 'name' """
    myCursor.execute(deleteHeaderSQL)
    myConnection.commit()
    # clean up
    myCursor.close()
    myConnection.close()
    myFile.close()
    myReader = None
    
print("Running SQL Question One")
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
    insertList = []
    checkList = []
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
                    if dist < 100.0:
                        #print str(y[2]) + " is less than 100 miles from " + str(tempCoord[2])                  
                        insertList.append(tuple([y[2],dist]))
#                        checkList.append(tuple())
#                        if len(insertList) % 5000 == 0:
#                            myCursor.executemany('INSERT INTO nearbyStores VALUES(?,?,?);',tempList)
#                            myConnection.commit()
#                            tempList =[]
#    myCursor.executemany('INSERT INTO nearbyStores VALUES(?,?,?);',tempList)
#    myConnection.commit()
#    print len(insertList)
    
    # delete the stores table if it already exists
    deleteSQLNearby = """ DROP TABLE IF EXISTS nearbyStores """
    myCursor.execute(deleteSQLNearby)
    myConnection.commit()
    myCursor.close()
    # create table for mcdonalds distance            
    createDistTableSQL = """ CREATE TABLE IF NOT EXISTS nearbyStores 
                         (storeNumber integer,
                         distance integer); """
    myCursor = myConnection.cursor()
    myCursor.execute(createDistTableSQL)    
    myConnection.commit()          
    
    
    # insert mcdonalds to database TODO
    tempList =[]
    for row in insertList:
        tempList.append(tuple(row))
        if len(tempList) % 5000 == 0:
            myCursor.executemany('INSERT INTO nearbyStores VALUES(?,?);',tempList)
            tempList =[]
            myConnection.commit()
    
    myCursor.executemany('INSERT INTO nearbyStores VALUES(?,?);',tempList)
    myConnection.commit()
    
    # cleanup
    myCursor.close()
    myConnection.close()
# haversine function calculates distance between two coordinate points
def haversine(lon1,lat1, lon2, lat2):
    
    lon1,lat1,lon2,lat2= map(radians, [lon1,lat1,lon2,lat2])
    
    dlon = lon2-lon1
    dlat = lat2-lat1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 
    return c *r
    

print("Running SQL Question Two")
sqlQuestionTwo()



def sqlQuestionThree():
    print("SQL Question Three is shown below in commented format and used in sqlQuestionOne")

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


sqlQuestionThree()
    
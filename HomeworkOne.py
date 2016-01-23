# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 23:05:28 2016

@author: Rob
"""

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
    import random
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
    import os
    import sqlite3
    import csv
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file = os.path.join(__location__, 'mcDonalds.csv')
    myConnection = sqlite3.connect('mcD.db')
    myCursor = myConnection.cursor()


    deleteSQL = """ DROP TABLE IF EXISTS STORES """
    
    myCursor.execute(deleteSQL)
    
    myConnection.commit()
    
    #create stores table
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
    
    myFile = open(__location__ + '\\mcDonalds.csv','rt')
    myReader = csv.reader(myFile)
    
    tempList = []
    
    for row in myReader:
        tempList.append(tuple(row))
        if len(tempList) % 5000 == 0:
            myCursor.executemany('INSERT INTO stores VALUES(?,?,?,?,?,?,?,?);',tempList)
            tempList =[]
            myConnection.commit()
            
    myCursor.close()
    myConnection.close()
    myFile.close()
    myReader = None
    

sqlQuestionOne()



    
# -*- coding: utf-8 -*-
# 1) Go to http://www.menuism.com/restaurant-locations and navigate to the Domino’s Pizza Locations.
# Write a Python script that does the following:
# - Scrapes menuism and gathers the following information for each Domino’s store in the United States: state, city, store number, and URL (Hint: use beautifulSoup and REGEX)
# - Creates a database that will hold the information you scraped
#  - Loads the information into a database '''

from bs4 import BeautifulSoup
import requests
import sqlite3

#Deal with DB stuff
dbName = 'dominos.db'
myConnection = sqlite3.connect(dbName)
myCursor = myConnection.cursor()

# delete the stores table if it already exists
deleteSQL = """ DROP TABLE IF EXISTS dominos """
myCursor.execute(deleteSQL)
myConnection.commit()
myCursor.close()

#create dominos table
myCursor = myConnection.cursor()
createTableSQL = """ CREATE TABLE IF NOT EXISTS dominos
(state text,
city text,
url text,
storeNumber integer); """
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
for state in stateUrl:
    currentState = requests.get(state)
    soupyState = BeautifulSoup(currentState.content)
    storeUrlList = soupyState.select('ul.list-unstyled-links a')

    for store in storeUrlList:
        print store



# iterate through stores within state


# get state city store number and URL



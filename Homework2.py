# -*- coding: utf-8 -*-
# 1) Go to http://www.menuism.com/restaurant-locations and navigate to the Domino’s Pizza Locations.
# Write a Python script that does the following:
# - Scrapes menuism and gathers the following information for each Domino’s store in the United States: state, city, store number, and URL (Hint: use beautifulSoup and REGEX)
# - Creates a database that will hold the information you scraped
#  - Loads the information into a database '''

from bs4 import BeautifulSoup
import requests
import re

# # Root dominos link to parse through
rootUrl = 'http://www.menuism.com/restaurant-locations/dominos-pizza-7144'
myPage = requests.get(rootUrl)
soup = BeautifulSoup(myPage.content)

# Get state urls from the root URL
# Store in stateURL List
stateUrl = []
storeUrlList = soup.select('.popular-cities-box li a')
for tags in storeUrlList:
    stateUrl.append(tags['href'])

# iterate through state


# iterate through stores within state

# get state city store number and URL



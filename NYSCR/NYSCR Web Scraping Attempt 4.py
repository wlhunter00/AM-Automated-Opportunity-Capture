# Important imports
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import pyodbc
# Connecting to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=US-NYC-NL000860\SQLEXPRESS;'
                      'Database=Opportunity Hunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


# Function that will simply truncate the table through python
# - mainly to make life easier
def truncateSQL(tableName):
    cursor.execute('truncate table ' + tableName)


# Pass in the number of pages you want to scrape and the amount of jobs you
# want to scrape. Returns an array of strings that will be passed through the
# url generator so that many pages can be scraped.
def calculatePageNumber(numberOfPages, jobsPerPage):
    runningCounter = 1
    startNum = [str(1)]
    for num in range(0, numberOfPages-1):
        runningCounter += jobsPerPage
        startNum.append(str(runningCounter))
    print(startNum)
    return startNum


# You pass in the name of the table you want to analyze. The function will then
# look at the table and find the last job inserted- allows for tables to be
# extended instead of overwritten each time
def findLastJob(tableName):
    cursor.execute('select max(jobID) from ' + tableName)
    columnMessage = str(cursor.fetchall()[0])
    if(columnMessage == '(None, )'):
        return 0
    else:
        locationComma = columnMessage.find(',')
        return int(columnMessage[1:locationComma])


# You want the URL to be very specific. Apply the filters on the site to
# get the exact url that you want. Insert the start which is the string we
# set above.

# Function takes in the name of the site we are scraping and the page number we
# are looking at. The urls will have to be hard coded, but doing it in a
# function will allow it to be modular. Returns the finished url to work with.
def getURL(site, startingNumber):
    if(site == 'NYSCR'):
        urlFromFunction = 'https://www.nyscr.ny.gov/adsOpen.cfm?startnum=' + startingNumber + '&orderBy=55&numPer=50&myAdsOnly=2&adClass=b&adCat=&adCounty=&adType=&mbe=0&wbe=0&dbe=0&keyword='
    return urlFromFunction


# Returns an array of job containers from the HTML. A job container is the
# closest HTML object you get to the information you want, that includes all of
# the information you need. Inputs are the url, the page number you want to
# scrape, how the object is defined and what the class name is. Should work for
# every type of site.
def getContainers(site, startingNumber, HTMLobject, className):
    url = getURL(site, startingNumber)
    # Just connecting to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.findAll(HTMLobject, class_=className)


# This hopefully works with many sites. Takes inputs, finds the items we want
# to import, and then uploads it to the SQL server. Container is found through
# getContainers(), labelHTML and resultHTML are the tag that they are
# classified as, there def's are the class name, databasename is the database
# that you want to insert into, pageNumber and site are self explanatory.
def searchAndUpload(container, labelHTML, resultHMTL, labelDef, resultDef,
                    databaseName, jobNumber, pageNumber, site):
    container_labels = container.findAll(labelHTML, class_=labelDef)
    container_results = container.findAll(resultHMTL, class_=resultDef)
    for num in range(0, len(container_labels)):
        cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                       + str(jobNumber).replace('\'', '\'\'') + '\', \''
                       + container_labels[num].text.replace('\'', '\'\'') + '\',  \''
                       + container_results[num].text.replace('\'', '\'\'') + '\',  \''
                       + site + '\')')
        conn.commit()
    cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                   + str(jobNumber).replace('\'', '\'\'') + '\', \''
                   + 'URL:' + '\',  \''
                   + getURL('NYSCR', pageNumber).replace('\'', '\'\'') + '\',  \''
                   + site + '\')')
    conn.commit()
    cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                   + str(jobNumber).replace('\'', '\'\'') + '\', \''
                   + 'dateInserted:' + '\',  \''
                   + datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace('\'', '\'\'') + '\',  \''
                   + site + '\')')
    conn.commit()


# The function that does all the work. Site is the specific site to analyze,
# database is the database you want to insert into, labelHTML, resultHTML, and
# containerHTML are the kind of HTML element these objects are, their defs are
# the classes of the HTML eleemnts. Number of pages and jobsPerPage are easy
def scrapeSite(site, database, labelHTML, resultHMTL, labelDef, resultDef,
               containerHTML, containerDef, numberOfPages, jobsPerPage):
    # Optional, clear the database
    truncateSQL(database)
    # Finds last job number in database and adds one
    jobNumber = findLastJob(database)+1
    # Start num is an array of page numbers
    startNum = calculatePageNumber(numberOfPages, jobsPerPage)
    # For loop that goes through the array. Basically allows us to run multiple
    # pages
    for start in startNum:
        # The job_containers is the HTML element that encompases every job.
        # Allows us to run multiple containers
        job_containers = getContainers(site, start, 'tr', 'r1')
        # A for loop that goes through all of the containers and extracts the
        # info from the specific job. The way this is done will differ for each
        # website
        for container in job_containers:
            # Collecting the information from the container and inserting it
            # into the SQL server
            searchAndUpload(container, labelHTML, resultHMTL, labelDef,
                            resultDef, database, jobNumber, start, site)
            # Incrase jobNumber as that is what is inserted into database
            jobNumber += 1
        # 1 second delay to avoid overtaxing the server
        time.sleep(1)


scrapeSite('NYSCR', 'NYSCRhybrid', 'div', 'div', "labelText", "resultText",
           'tr', 'r1', 2, 50)

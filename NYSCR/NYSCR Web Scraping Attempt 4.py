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

def truncateSQL(tableName):
    cursor.execute('truncate table ' + tableName)


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
def getURL(site, startingNumber):
    if(site == 'NYSCR'):
        url = 'https://www.nyscr.ny.gov/adsOpen.cfm?startnum=' + startingNumber + '&orderBy=55&numPer=50&myAdsOnly=2&adClass=b&adCat=&adCounty=&adType=&mbe=0&wbe=0&dbe=0&keyword='
    return url


def getContainers(site, startingNumber, HTMLobject, className):
    url = getURL(site, startingNumber)
    # Just connecting to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.findAll(HTMLobject, class_=className)


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


# 1 and 50 are the pages we want to start at. str() casts these as strings
def testFunction():
    truncateSQL('NYSCRhybrid')
    jobNumber = findLastJob('NYSCRhybrid')+1
    startNum = [str(1), str(50)]
    # For loop that goes through the array. Basically allows us to run multiple
    # pages
    for start in startNum:
        # The job_containers is the HTML element that encompases every job.
        # Allows us to run multiple containers
        # job_containers = soup.findAll('tr', class_='r1')
        job_containers = getContainers('NYSCR', start, 'tr', 'r1')
        # A for loop that goes through all of the containers and extracts the
        # info from the specific job. The way this is done will differ for each
        # website
        for container in job_containers:
            # Collecting the information from the container
            # Insert text block plus URL into SQL table
            searchAndUpload(container, 'div', 'div', "labelText", "resultText",
                            'NYSCRhybrid', jobNumber, start, 'NYSC')
            # container_labels = container.findAll('div', class_="labelText")
            # container_results = container.findAll('div', class_="resultText")
            # for num in range(0, len(container_labels)):
            #     cursor.execute('INSERT into NYSCRhybrid (jobID, labelText, resultText) VALUES (\''
            #             + str(jobNumber).replace('\'','\'\'') + '\', \''
            #                     + container_labels[num].text.replace('\'','\'\'') + '\',  \''
            #                             + container_results[num].text.replace('\'','\'\'') + '\')')
            #     conn.commit()
            # cursor.execute('INSERT into NYSCRhybrid (jobID, labelText, resultText) VALUES (\''
            #         + str(jobNumber).replace('\'','\'\'') + '\', \''
            #                 + 'URL:' + '\',  \''
            #                         + getURL('NYSCR', start).replace('\'','\'\'') + '\')')
            # conn.commit()
            # cursor.execute('INSERT into NYSCRhybrid (jobID, labelText, resultText) VALUES (\''
            #         + str(jobNumber).replace('\'','\'\'') + '\', \''
            #                 + 'dateInserted:' + '\',  \''
            #                         + datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace('\'','\'\'') + '\')')
            # conn.commit()
            jobNumber += 1
        # 1 second delay to avoid overtaxing the server
        time.sleep(1)


testFunction()

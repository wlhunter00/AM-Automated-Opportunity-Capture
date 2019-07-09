# Important imports
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pyodbc
# Connecting to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=jackson;'
                      'Database=OppHunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


# Function that will simply truncate the table through python
# - mainly to make life easier
def truncateSQL(tableName):
    cursor.execute('truncate table ' + tableName)


def cleanRawSQL(site):
    if(site == 'NYSCR'):
        cursor.execute("select * from NYSCR_raw where labelText like '%Due%'")
        cursor.execute("update NYSCR_raw set labelText = 'Due Date:' where labelText like '%Due%' or labelText like '%End%'")
        cursor.execute("update NYSCR_raw set labelText = 'Company:' where labelText like '%Agency%'")
        conn.commit()
    elif(site == 'DASNY'):
        cursor.execute("update DASNY_raw set resultText = substring(resultText, 0, CHARINDEX(' ', resultText)) where labelText like '%Due%'")
        conn.commit()
    elif(site == 'GOVUK'):
        cursor.execute("update GOVUK_raw set [resultText] = substring([resultText], 5, 2) + '/' + substring([resultText], 2, 2) + '/' + substring([resultText], 8, 4) where [labelText] like '%Closing%' or [labelText] like '%Publication%';")
        conn.commit()
    elif(site == 'RFPDB'):
        cursor.execute("update RFPDB_raw set resultText = substring(resultText,0, 11) where labelText = 'endDate'")
        conn.commit()


# Pass in the number of pages you want to scrape and the amount of jobs you
# want to scrape. Returns an array of strings that will be passed through the
# url generator so that many pages can be scraped.
def calculatePageNumber(numberOfPages, jobsPerPage, site):
    if(site == 'NYSCR'):
        runningCounter = 1
        startNum = [str(1)]
        for num in range(0, numberOfPages-1):
            runningCounter += jobsPerPage
            startNum.append(str(runningCounter))
    elif(site == 'DASNY'):
        runningCounter = 0
        startNum = [str(0)]
        for num in range(0, numberOfPages-1):
            runningCounter += 1
            startNum.append(str(runningCounter))
    elif(site == 'GOVUK' or site == 'RFPDB'):
        runningCounter = 1
        startNum = [str(1)]
        for num in range(0, numberOfPages-1):
            runningCounter += 1
            startNum.append(str(runningCounter))
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
    elif(site == 'DASNY'):
        urlFromFunction = 'https://www.dasny.org/opportunities/rfps-bids?field_solicitation_classificatio_target_id=All&field_solicitation_type_target_id=All&field_goals_target_id=All&field_set_aside_target_id=All&query=&page=' + startingNumber
    elif(site == 'GOVUK'):
        urlFromFunction = 'https://www.contractsfinder.service.gov.uk/Search/Results?&page='+ startingNumber + '#dashboard_notices'
    elif(site == 'RFPDB'):
        urlFromFunction = 'http://www.rfpdb.com/view/category/name/technology/page/' + startingNumber
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
    if(getScrapingCase(site) == 'RFPDB'):
        return soup.select('li[itemtype="http://schema.org/CreativeWork/RequestForProposal"]')
    else:
        return soup.findAll(HTMLobject, class_=className)


def getDatabase(site):
    return [site + '_raw', site + '_pvt']


def getScrapingCase(site):
    if(site == 'NYSCR' or site == 'DASNY'):
        return 'TwoTags'
    elif(site == 'GOVUK'):
        return 'OneTag'
    elif(site == 'RFPDB'):
        return 'RFPDB'


def getURLCase(site):
    if(site == 'NYSCR'):
        return 'noURL'
    elif(site == 'DASNY' or site == 'GOVUK' or site == 'RFPDB'):
        return 'seperateURL'


def listScrape(container, site, type):
    tempList = []
    if(site == 'RFPDB'):
        if(type == 'labels'):
            tempList.append(container.find('span', class_='comment')['itemprop'])
            tempList.append(container.find('time')['itemprop'])
            tempList.append('Location')
            tempList.append('Categories')
        if(type == 'results'):
            tempList.append(container.find('span', class_='comment').text)
            tempList.append(container.find('time')['datetime'])
            tempList.append(container.select_one('span[itemprop="address"]').text)
            tempList.append(container.find('ul', class_='categories').text)
    return tempList


# This hopefully works with many sites. Takes inputs, finds the items we want
# to import, and then uploads it to the SQL server. Container is found through
# getContainers(), labelHTML and resultHTML are the tag that they are
# classified as, there def's are the class name, databasename is the database
# that you want to insert into, pageNumber and site are self explanatory.
def searchAndUpload(container, labelHTML, resultHTML, labelDef, resultDef,
                    databaseName, jobNumber, pageNumber, site):
    if(getScrapingCase(site) == 'RFPDB'):
        container_labels = listScrape(container, site, 'labels')
        container_results = listScrape(container, site, 'results')

    else:
        container_labels = container.findAll(labelHTML, class_=labelDef)
        if(getScrapingCase(site) == 'TwoTags'):
            container_results = container.findAll(resultHTML, class_=resultDef)

    for num in range(0, len(container_labels)):
        if(getScrapingCase(site) == 'OneTag'):
            cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                           + str(jobNumber).replace('\'', '\'\'') + '\', \''
                           + container_labels[num].find(resultHTML, class_=resultDef).text.replace('\'', '\'\'') + '\',  \''
                           + container_labels[num].find(resultHTML, class_=resultDef).next_sibling.replace('\'', '\'\'') + '\',  \''
                           + site + '\')')
            conn.commit()

        elif(getScrapingCase(site) == 'TwoTags'):
            cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                           + str(jobNumber).replace('\'', '\'\'') + '\', \''
                           + container_labels[num].text.replace('\'', '\'\'') + '\',  \''
                           + container_results[num].text.replace('\'', '\'\'') + '\',  \''
                           + site + '\')')
            conn.commit()
        elif(getScrapingCase(site) == 'RFPDB'):
            cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                           + str(jobNumber).replace('\'', '\'\'') + '\', \''
                           + container_labels[num].replace('\'', '\'\'') + '\',  \''
                           + container_results[num].replace('\'', '\'\'') + '\',  \''
                           + site + '\')')
            conn.commit()

    if(site == 'DASNY'):
        title = container.find('div', class_='rfp-bid-title')
        link = 'https://www.dasny.org' + title.find('a')['href']

    elif(site == 'RFPDB'):
        title = container.find('a')
        link = 'http://www.rfpdb.com' + container.find('a')['href']

    elif(site == 'GOVUK'):
        title = container.find('div', class_='search-result-header')
        link = title.find('a')['href']
        company = container.find('div', class_='search-result-sub-header wrap-text')
        cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                       + str(jobNumber).replace('\'', '\'\'') + '\', \''
                       + 'Company:' + '\',  \''
                       + company.text.replace('\'', '\'\'') + '\',  \''
                       + site + '\')')
        conn.commit()
        if(container.find('span', class_='') is not None):
            cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                           + str(jobNumber).replace('\'', '\'\'') + '\', \''
                           + 'Description:' + '\',  \''
                           + container.find('span', class_='').text.replace('\'', '\'\'') + '\',  \''
                           + site + '\')')
            conn.commit()

    if(getURLCase(site) == 'noURL'):
        cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                       + str(jobNumber).replace('\'', '\'\'') + '\', \''
                       + 'URL:' + '\',  \''
                       + getURL(site, pageNumber).replace('\'', '\'\'') + '\',  \''
                       + site + '\')')
        conn.commit()

    elif(getURLCase(site) == 'seperateURL'):
        cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                       + str(jobNumber).replace('\'', '\'\'') + '\', \''
                       + 'URL:' + '\',  \''
                       + link.replace('\'', '\'\'') + '\',  \''
                       + site + '\')')
        conn.commit()
        cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                       + str(jobNumber).replace('\'', '\'\'') + '\', \''
                       + 'Title:' + '\',  \''
                       + title.text.replace('\'', '\'\'') + '\',  \''
                       + site + '\')')
        conn.commit()

    cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, resultText, website) VALUES (\''
                   + str(jobNumber).replace('\'', '\'\'') + '\', \''
                   + 'dateInserted:' + '\',  \''
                   + datetime.now().strftime('%m/%d/%Y %H:%M:%S').replace('\'', '\'\'') + '\',  \''
                   + site + '\')')
    conn.commit()


# The function that does all the work. Site is the specific site to analyze,
# database is the database you want to insert into, labelHTML, resultHTML, and
# containerHTML are the kind of HTML element these objects are, their defs are
# the classes of the HTML eleemnts. Number of pages and jobsPerPage are easy
def scrapeSite(site, labelHTML, resultHMTL, labelDef, resultDef,
               containerHTML, containerDef, numberOfPages, jobsPerPage):
    # Optional, clear the database
    databases = getDatabase(site)
    truncateSQL(databases[0])
    # Finds last job number in database and adds one
    jobNumber = findLastJob(databases[0])+1
    # Start num is an array of page numbers
    startNum = calculatePageNumber(numberOfPages, jobsPerPage, site)
    # For loop that goes through the array. Basically allows us to run multiple
    # pages
    for start in startNum:
        # The job_containers is the HTML element that encompases every job.
        # Allows us to run multiple containers
        job_containers = getContainers(site, start, containerHTML, containerDef)
        # A for loop that goes through all of the containers and extracts the
        # info from the specific job. The way this is done will differ for each
        # website
        for container in job_containers:
            # Collecting the information from the container and inserting it
            # into the SQL server
            searchAndUpload(container, labelHTML, resultHMTL, labelDef,
                            resultDef, databases[0], jobNumber, start, site)
            # Incrase jobNumber as that is what is inserted into database
            jobNumber += 1
        print('Scraped: ' + site + " - Page " + start)
    cleanRawSQL(site)
    print(site + ' Completed')


scrapeSite('NYSCR', 'div', 'div', "labelText", "resultText",
           'tr', 'r1', 2, 50)
scrapeSite('DASNY', 'td', 'td', '', 'fieldValue',
           'div', 'views-field views-field-nothing-1', 2, 10)
scrapeSite('GOVUK', 'div', 'strong', 'search-result-entry', '',
           'div', 'search-result', 50, 20)
scrapeSite('RFPDB', '', '', '', '',
           '', '', 20, 12)
cursor.close()
conn.close()
print('All sites scraped')

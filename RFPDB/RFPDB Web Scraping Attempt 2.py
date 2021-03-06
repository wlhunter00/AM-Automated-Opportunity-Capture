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


# Given a file, it will execute any .sql files.
def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
            conn.commit()
            print(str(command) + " excecuted.")
        except:
            print("Command skipped: " + str(command))


# Pass in the number of pages you want to scrape and the amount of jobs you
# want to scrape. Returns an array of strings that will be passed through the
# url generator so that many pages can be scraped.
def calculatePageNumber(numberOfPages, jobsPerPage, site):
    if(site == 'DASNY'):
        runningCounter = 0
        startNum = [str(0)]
    else:
        runningCounter = 1
        startNum = [str(1)]
    for num in range(0, numberOfPages-1):
        if(site == 'NYSCR'):
            runningCounter += jobsPerPage
        else:
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
def getURL(site, startingNumber, category):
    if(site == 'NYSCR'):
        urlFromFunction = 'https://www.nyscr.ny.gov/adsOpen.cfm?startnum=' + startingNumber + '&orderBy=55&numPer=50&myAdsOnly=2&adClass=b&adCat=&adCounty=&adType=&mbe=0&wbe=0&dbe=0&keyword='
    elif(site == 'DASNY'):
        urlFromFunction = 'https://www.dasny.org/opportunities/rfps-bids?field_solicitation_classificatio_target_id=All&field_solicitation_type_target_id=All&field_goals_target_id=All&field_set_aside_target_id=All&query=&page=' + startingNumber
    elif(site == 'GOVUK'):
        urlFromFunction = 'https://www.contractsfinder.service.gov.uk/Search/Results?&page='+ startingNumber + '#dashboard_notices'
    elif(site == 'RFPDB'):
        urlFromFunction = 'http://www.rfpdb.com/view/category/name/'+ category + '/page/' + startingNumber
    return urlFromFunction


# Returns an array of job containers from the HTML. A job container is the
# closest HTML object you get to the information you want, that includes all of
# the information you need. Inputs are the url, the page number you want to
# scrape, how the object is defined and what the class name is. Should work for
# every type of site.
def getContainers(site, startingNumber, HTMLobject, className, category):
    url = getURL(site, startingNumber, category)
    # Just connecting to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    if(getScrapingCase(site) == 'RFPDB'):
        return soup.select('li[itemtype="http://schema.org/CreativeWork/RequestForProposal"]')
    else:
        return soup.findAll(HTMLobject, class_=className)


# Given the name of the site returns a list of two database names, the raw and
# Pivot tables
def getDatabase(site):
    return [site + '_raw', site + '_pvt']


# Given a site, returns the scraping case
def getScrapingCase(site):
    if(site == 'NYSCR' or site == 'DASNY'):
        return 'TwoTags'
    elif(site == 'GOVUK'):
        return 'OneTag'
    elif(site == 'RFPDB'):
        return 'RFPDB'


# Given the site, gives a URL case
def getURLCase(site):
    if(site == 'NYSCR'):
        return 'noURL'
    else:
        return 'seperateURL'


# Brute force scraping method if the website doesn't use the common labels.
# Will be different for every site. Has to be run twice, once for labels and
# another time for results, returns a list of those items.
def listScrape(container, site, type):
    tempList = []
    # Case exclusivley for RFPDB
    if(site == 'RFPDB'):
        if(type == 'labels'):
            tempList.append(container.find('span',
                                           class_='comment')['itemprop'])
            tempList.append(container.find('time')['itemprop'])
            tempList.append('Location:')
            tempList.append('Categories:')
        if(type == 'results'):
            tempList.append(container.find('span', class_='comment').text)
            tempList.append(container.find('time')['datetime'])
            tempList.append(container.select_one('span[itemprop="address"]').text)
            tempList.append(container.find('ul', class_='categories').text)
    return tempList


# Given the database name, it will input the information into a raw table in
# the correct format, and then commit the command. We want to replace the back-
# slashes because of python viewing it as an escape character.
def insertIntoSQL(databaseName, jobNumber, label, result, site):
    cursor.execute('INSERT into ' + databaseName + ' (jobID, labelText, '
                   + 'resultText, website) VALUES (\''
                   + str(jobNumber).replace('\'', '\'\'') + '\', \''
                   + label.replace('\'', '\'\'') + '\',  \''
                   + result.replace('\'', '\'\'') + '\',  \''
                   + site + '\')')
    conn.commit()


# Takes inputs, finds the items we want to import, and then uploads it to the
# SQL server. Container is found through getContainers(), labelHTML and
# resultHTML are the tag that they are classified as, there def's are the class
# name, databasename is the database that you want to insert into, pageNumber
# and site are self explanatory. Calls insertIntoSQL a lot to insert this info.
def searchAndUpload(container, labelHTML, resultHTML, titleHTML, labelDef,
                    resultDef, titleDef, databaseName, jobNumber, pageNumber,
                    site):
    # RFPDs hardcode scrape
    if(getScrapingCase(site) == 'RFPDB'):
        container_labels = listScrape(container, site, 'labels')
        container_results = listScrape(container, site, 'results')

    else:
        # Every other site has a label container
        container_labels = container.findAll(labelHTML, class_=labelDef)
        if(getScrapingCase(site) == 'TwoTags'):
            # If it is a site with a label and result tag format then it is
            # two tag.
            container_results = container.findAll(resultHTML, class_=resultDef)
    # Scraping title
    title = container.find(titleHTML, class_=titleDef)
    # Run an array through all of the scraped info
    for num in range(0, len(container_labels)):
        # If it has one tag we want to insert the item, then the sibiling items
        # found in the HTML.
        if(getScrapingCase(site) == 'OneTag'):
            insertIntoSQL(databaseName, jobNumber,
                          container_labels[num].find(resultHTML, class_=resultDef).text,
                          container_labels[num].find(resultHTML, class_=resultDef).next_sibling,
                          site)
        # If it has two tags just submit the labels and results
        elif(getScrapingCase(site) == 'TwoTags'):
            insertIntoSQL(databaseName, jobNumber, container_labels[num].text,
                          container_results[num].text, site)
        # Since RFPDB is hard coded, the list are strings, so no need for .text
        elif(getScrapingCase(site) == 'RFPDB'):
            insertIntoSQL(databaseName, jobNumber, container_labels[num],
                          container_results[num], site)
    # Getting site and link based on the websites case.
    if(site == 'DASNY'):
        link = 'https://www.dasny.org' + title.find('a')['href']
    elif(site == 'RFPDB'):
        link = 'http://www.rfpdb.com' + container.find('a')['href']
    # With GOVUK we can also pull out the company and description doing hard
    # scraping and inserting it into table individually.
    elif(site == 'GOVUK'):
        link = title.find('a')['href']
        company = container.find('div',
                                 class_='search-result-sub-header wrap-text')
        insertIntoSQL(databaseName, jobNumber, 'Company:', company.text, site)
        if(container.find('span', class_='') is not None):
            insertIntoSQL(databaseName, jobNumber, 'Description:',
                          container.find('span', class_='').text, site)
    # Insert URL and title if the url is seperate
    if(getURLCase(site) == 'seperateURL'):
        insertIntoSQL(databaseName, jobNumber, 'URL:', link, site)
        insertIntoSQL(databaseName, jobNumber, 'Title:', title.text, site)
    # If there is no URL just insert where the page we scraped
    elif(getURLCase(site) == 'noURL'):
        insertIntoSQL(databaseName, jobNumber, 'URL:',
                      getURL(site, pageNumber), site)
    # For every job insert the time it was scraped
    insertIntoSQL(databaseName, jobNumber, 'dateInserted:',
                  datetime.now().strftime('%m/%d/%Y %H:%M:%S'), site)


# The function that does all the work. Site is the specific site to analyze,
# database is the database you want to insert into, labelHTML, resultHTML, and
# containerHTML are the kind of HTML element these objects are, their defs are
# the classes of the HTML eleemnts. Number of pages and jobsPerPage are easy
def scrapeSite(site, labelHTML, resultHMTL, labelDef, resultDef,
               containerHTML, containerDef, titleHTML, titleDef, numberOfPages,
               jobsPerPage):
    # Get table names
    databases = getDatabase(site)
    # Finds last job number in database and adds one
    jobNumber = findLastJob(databases[0])+1
    # Start num is an array of urls
    startNum = calculatePageNumber(numberOfPages, jobsPerPage, site)
    # For loop that goes through the array. Basically allows us to run multiple
    # pages
    for start in startNum:
        # The job_containers is the HTML element that encompases every job.
        # Allows us to run multiple containers
        job_containers = getContainers(site, start, containerHTML, containerDef, labelHTML)
        # A for loop that goes through all of the containers and extracts the
        # info from the specific job. The way this is done will differ for each
        # website
        for container in job_containers:
            # Collecting the information from the container and inserting it
            # into the SQL server
            searchAndUpload(container, labelHTML, resultHMTL, titleHTML,
                            labelDef,  resultDef, titleDef, databases[0],
                            jobNumber, start, site)
            # Incrase jobNumber as that is what is inserted into database
            jobNumber += 1
        print('Scraped: ' + site + " - Page " + start)
    print(site + ' Completed')
scrapeSite('NYSCR', 'div', 'div', "labelText", "resultText",
           'tr', 'r1', '', '', 2, 50)
scrapeSite('DASNY', 'td', 'td', '', 'fieldValue',
           'div', 'views-field views-field-nothing-1', 'div', 'rfp-bid-title',
            2, 10)
scrapeSite('GOVUK', 'div', 'strong', 'search-result-entry', '',
           'div', 'search-result', 'div', 'search-result-header', 50, 20)
RFPDBCategories = pd.read_sql_query('select * from RFPDBCategories_tbl', conn)
for index, row in RFPDBCategories.iterrows():
    scrapeSite('RFPDB', row["category"], '', '', '',
               '', '', '', 'a', row["pageNumbers"], 12)
    print('RFPDB - ' + row["category"] + ' - completed.')
print('All sites scraped.')
executeScriptsFromFile("C:\\Users\\whunter\Documents\\GitHub\\AM-Automated-Oppurtinity-Capture\\SQL Scripts\\cleanRawSQL.sql")
print('All tables cleaned.')
print('Master Function Complete.')
cursor.close()
conn.close()

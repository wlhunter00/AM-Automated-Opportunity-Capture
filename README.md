# AM Automated Opportunity Capture
## Introduction
This is the automated oppourtunity hunter for Alvarez and Marsal's Forensic Technology Services team.
The tool will go out to sites requested by the team, and will scrape information about various
RFPs, RFIs, networking events, and various other opportunities that could result in more projects for the team. After this information is scraped, it is stored in a SQL database, and then a daily report
on the tools findings will be emailed to the team.

#### Process
1. Scrape all RFP sites using the Python library BeautifulSoup.
2. Insert this data into a raw SQL table.
3. Scrape all event sites using their API through python.
4. Insert this data into a raw SQL table.
5. Clean the invidual tables using SQL queries.
6. Insert all indivdual sites into master table and current table.
7. Using Pandas take SQL queries and insert the data in dataframe.
8. Export the dataframes into excel sheets.
9. Attach the excel sheet and email the team the results using Yagmail and HMTL.

## Table of Contents
* [Project Status](#project-status)
  * [To Do](#to-do)
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Installation](#installation)
* [Walkthroughs](#Walkthroughs)
  * [File Walkthroughs](#files-walkthrough)
  * [Python Master Function Walkthrough](#Python-Master-Function-Walkthrough)
    * [Scraping Main Functions](#Scraping-main-functions)
    * [Scraping Helping Functions](#Scraping-Helping-Functions)
    * [Exporting Helping Functions](#Exporting-Helping-Functions)
* [Adding a Site](#adding-a-site)
* [Typical Errors](#typical-errors)

## Project Status
###### **Version 1.2**

Stable build is currently ready. Automated reports sent out daily. Functionality is currently being expanded on.

###### **Recently Added**
Added scraped events from Eventbrite to the daily report.

#### To Do:
- [ ] Correctly spell Opportunity everywhere.
- [ ] Create this README.
- [ ] Create Presentation.
- [ ] Look to implement dictionaries.
- [ ] Make sure there aren't uneeded loops in main script.
- [ ] Scrape 10Times.com using infinite scrolling.
- [ ] Use FBO.gov's API to scrape their RFPs.
- [ ] Decentralize the PATHs.

## Technologies
Project was created with:
- Python Version: 3.6
  - BeautifulSoup
  - Pyodbc
  - Pandas
  - Yagmail
  - Requests
- Microsoft SQL Server
- HTML

## Installation
For this to fully work, the application needs to be run on a **MAGNUS** computer, as the inserts into the SQL database need to be accessed on the remote desktop.

First, you  need to install [Python 3.7.1](https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe) (you need to have a python version 3.0+). I use [ATOM](https://atom.io/download/windows_x64) as my text editor, by any works.

Then you are going to set your PATH and ```python -m pip install``` in the command prompt the following libraries:

1. datetime
2. bs4
3. Pyodbc
4. Yagmail
5. Pandas
6. glob
7. os
8. requests

(Optionally) you can install [Microsoft SQL Server](https://go.microsoft.com/fwlink/?linkid=853017) to view the data yourself and to debug.

The most important files to have on your computer are the [Python Master Function](https://github.com/wlhunter00/AM-Automated-Oppurtinity-Capture/blob/master/Python%20Code/Python%20Master%20Function.py), [Master SQL Query](https://github.com/wlhunter00/AM-Automated-Oppurtinity-Capture/blob/master/SQL%20Scripts/Master%20Function%20Query.sql), [Clean Raw SQL Query](https://github.com/wlhunter00/AM-Automated-Oppurtinity-Capture/blob/master/SQL%20Scripts/cleanRawSQL.sql), and the [SQL to Python Keywords](https://github.com/wlhunter00/AM-Automated-Oppurtinity-Capture/blob/master/SQL-Python%20Keywords%20Queries.txt) files. Finally you will need the **Email Information** text file. This file is not found in the Github, as it contains sensative information.
## Walkthroughs

### Files Walkthrough:
- The first folders house the files used to develop the scraping algorithms for the indivdual sites (10Times, DASNY, GOVUK, NYSCR, RFPDB).
- The Excel Sheets folder houses the export sheets from this application.
- The Presentation Photos were simply used for screenshots.
- The Weekly Reports house the powerpoint presentations I have created throughout the internship.
- The folder Python Code houses all of the python scripts, the most important one being the [Python Master Function](https://github.com/wlhunter00/AM-Automated-Oppurtinity-Capture/blob/master/Python%20Code/Python%20Master%20Function.py).
- The folder SQL scripts houses all of the SQL server queries, the most important ones being the [Master SQL Query](https://github.com/wlhunter00/AM-Automated-Oppurtinity-Capture/blob/master/SQL%20Scripts/Master%20Function%20Query.sql), and the [Clean Raw SQL Query](https://github.com/wlhunter00/AM-Automated-Oppurtinity-Capture/blob/master/SQL%20Scripts/cleanRawSQL.sql).

### Python Master Function Walkthrough:
- Starts with importing the libraries mentioned in [Installation](#installation).
- Connects to SQL server.
- Creates lists to store information.
- ```def mainFunction():``` The main function of the script that will call all of the important functions and complete the process.
  - Parameters: None.
  - Returns: Nothing.
  - Called by: None

#### **Scraping Main Functions**
  - ```def searchAndUpload(container, labelHTML, resultHTML, titleHTML, labelDef, resultDef, titleDef, databaseName, jobNumber, pageNumber, site):``` Will scrape all of the relevant information from a job, and then upload this information to an SQL raw table.
    - Walkthrough: Very case based. First you scrap the jobs information using the HTML and class definitions (or hard code scrape it). Then you loop through the whole list and insert this information into SQL. Then based on the sites and the cases you insert specific information into the SQL table.
    - Parameters: Takes in a job (container), the HTML and class of the label, result, and title information, the name of the table, the job number and website.
    - Returns: Nothing.
    - Called by ```scrapeSite```
  - ```def scrapeSite(site, labelHTML, resultHMTL, labelDef, resultDef, containerHTML, containerDef, titleHTML, titleDef, numberOfPages, jobsPerPage):``` Main function used for web scraping.
    - Walkthrough: First we get the needed information such as the database names, the starting number, and array of page numbers. Then for each page we get a list of jobs. Then for each job we scrape and upload.
    - Parameters: The website, HTML and class for the label, result, container, and the number of pages and jobs per page.
    - Returns: Nothing.
    - Called by ```mainFunction```
  - ```def scrapeEventbrite():``` Scrapes information from Eventbrites API and uploads it to SQL.
    - Walkthrough: First give the categories to scrape. Then for each category find the number of pages of events there are. Then loop through each event and insert the given information into the table.
    - Parameters: Nothing.
    - Returns: Nothing.
    - Called by: ```mainFunction```
  - ```def executeScriptsFromFile(filename):``` Executes SQL query from a file. Used with ```cleanRawSQL``` and ```masterSQLFunction```.
    - Walkthrough: Opens the SQL file, splits each command by find the ';', and then runs each command.
    - Parameters: The location of the SQL query we want to run.
    - Returns: Nothing.
    - Called by: ```mainFunction```

#### **Scraping Helping Functions**
  - ```def removeEscape(text):``` removes the escape character for SQL inserts.
    - Parameters: Takes in string to parse.
    - Returns: Changed string.
    - Called by: ```insertIntoSQL```, ```scrapeEventbrite```
  - ```def parseASCII(text):``` parses out non-ascii characters.
    - Parameters: Takes in string to parse.
    - Returns parsed string.
    - Called by: ```insertIntoSQL```, ```scrapeEventbrite```
  - ```def calculatePageNumber(numberOfPages, jobsPerPage, site):``` Creates an array of page numbers for the url.
    - Parameters: Takes in the number of pages and the jobs per page, and the site.
    - Returns: An array of page numbers to parsed.
    - Called by: ```scrapeSite```
  - ```def findLastJob(tableName):``` Finds last job in tables.
    - Parameters: Table to look at.
    - Returns: ID of the last jobs.
    - Called by: ```scrapeSite```
  - ```def getURL(site, startingNumber, category):``` Gives the URL to scrape from. Has to be hardcoded.
    - Parameters: Site to scrape, the page number, and the category we are looking at.
    - Returns: URL to scrape.
    - Called by: ```getContainers```
  - ```def getContainers(site, startingNumber, HTMLobject, className, category):``` Gives array of indivdual jobs to scrape from the given page
    - Parameters: All the information needed to retrieve the URL, and the class HTML and ID of the job object. See [Adding a Site](#adding-a-site).
    - Returns: List of jobs to be scraped individually.
    - Called by: ```scrapeSite```
  - ```def getDatabase(site):``` Gives the database names based on the sites.
    - Parameters: Name of the website.
    - Returns: List of the Database names, the raw and piviot tables.
    - Called by: ```scrapeSite```
  - ```def getScrapingCase(site):``` Gives the scraping case for each website. Has to be hardcoded.
    - Parameters: Name of the site.
    - Returns: Name of the scraping case.
    - Called by: ```searchAndUpload```, ```getContainers```
  - ```def getURLCase(site):``` Gives the URL case for each website. Has to be hardcoded.
    - Parameters: Name of the site.
    - Returns: Name of the URL case.
    - Called by: ```searchAndUpload```
  - ```def listScrape(container, site, type):``` The hardcoded method to scrape a site, when the information we are looking for is super specific. So far only used for RFPDB. Usually has to be called twice, once to return a list of labels and another time to return a list of results.
    - Parameters: The job we are looking at, the site, and if we are looking for labels or results
    - Returns: A list containing the given information to be stored.
    - Called by: ```searchAndUpload```
  - ```def insertIntoSQL(databaseName, jobNumber, label, result, site):``` Inserts given information into SQL table.
    - Parameters: Table to insert into, job number, label of information, the information, and the website.
    - Returns: Nothing.
    - Called by: ```searchAndUpload```

#### **Exporting Main Functions**
- ```def queryToExcelSheet():``` Will create an excel file from SQL queries.
  - Walkthrough: First we grab the SQL queries we want to use from the text file, then we load the data from the SQL tables into a dataframe, then we take this data and put it into two different excel spreadsheets, one is updating the master sheet and one is the daily excel file.
  - Parameters: None.
  - Returns: Nothing.
  - Called by: ```mainFunction```
- ```def sendEmail():``` Sends email to the team using a premade gmail account. Attached is the excel file that was created.
  - Walkthrough: First we open up the email login file, then we find the latest created excel file, then we create the body of the email, the HTML variable is the table that is created, as shown below. This is all then loaded on an yagmail object and sent to all the email addresses we want.
  <br><img src="https://github.com/wlhunter00/AM-Automated-Oppurtinity-Capture/blob/master/Images%20for%20Readme/Example%20Table.PNG"><br>
  - Parameters: None.
  - Returns: Nothing.

#### **Exporting Helping Functions**
  - ```def splitKeyWordFile():``` Opens up the keyword file and fills the queries and sheets list.
    - Parameters:  None
    - Returns: Technically nothing, but fills both the queries and sheets lists. The queries list specifies what data will be inserted into the excel sheet and the sheets list is the name of that sheet.
    - Called by: ```queryToExcelSheet```
  - ```def loadDataFrames():``` Loads list of dataframes that is made up of the list of queries
    - Parameters: Technically nothing, but uses list of queries from ```splitKeyWordFile```
    - Returns: Technically nothing, but fills dataFrames list with the result from the select query.
    - Called by: ```queryToExcelSheet``
  - ```def loadCountingFrames():``` For the keyword queries, loads list of ints for how many new records were added
    - Parameters: None.
    - Returns: Technically nothing but fills array with how many new records have been inserted.
    - Called by: ```mainFunction```
  - ```def writeToExcel(writer):``` Will write a dataframe into an excel spreadsheet. Loops through all of the queries.
    - Parameters: Takes in a writer, which is basically an excel document.
    - Returns: Nothing.
    - Called by: ```queryToExcelSheet```

## Adding a Site

## Typical Errors
- Creating failures
- No email is getting sent
- Person in specific recieving emails
- No jobs are being shown as added.

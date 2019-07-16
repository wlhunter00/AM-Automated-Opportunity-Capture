import requests
import string
import pyodbc
from datetime import datetime

# Connecting to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=jackson;'
                      'Database=OppHunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


# Removes escape characters
def removeEscape(text):
    return text.replace('\'', '\'\'')


# Gets rid of non ascii characters in string
def parseASCII(text):
    if(text is not None):
        return ''.join(filter(lambda x: x in string.printable, text))
    else:
        return ''


# Scrapes eventbrite's API and sends data to SQL
def scrapeEventbrite():
    # Array of categories to go through
    categoriesToScrap = ["101", "102", "112"]

    # loop through all the categories
    for category in categoriesToScrap:
        # Obtaining the JSON of the details of the category to know how many pages
        pageNumParam = {"categories": category, "location.address": "NewYork",
                      "location.within": "8mi", "token": "4DYO5EC3JABSP5NVOGOX"}
        pagenumJSON = requests.get('https://www.eventbriteapi.com/v3/events/search',
                                      pageNumParam).json()
        numPages = int(pagenumJSON['pagination']['page_count'])
        # Setting the category to a word for SQL
        if(category == "101"):
            stringCategory = "Business"
        elif(category == "102"):
            stringCategory = "Technology"
        elif(category == "112"):
            stringCategory = "Government"
        # Pass through all the pages in category
        for pageNumber in range(1, numPages):
            # Retrieving details from API
            eventParam = {"categories": category, "location.address": "NewYork",
                          "location.within": "8mi", "expand": "venue",
                          "page": pageNumber, "token": "4DYO5EC3JABSP5NVOGOX"}
            eventJSON = requests.get('https://www.eventbriteapi.com/v3/events/search',
                                        eventParam).json()
            # Run through each event on the page
            for i in eventJSON['events']:
                # inserting the data into SQL
                cursor.execute('INSERT into eventBrite_raw (Title, shortSummary, longSummary, '
                               + 'URL, eventStart, eventEnd, publishDate, status, onlineEvent, insertDate, category, address) VALUES (\''
                               + removeEscape(parseASCII(i['name']['text'])) + '\', \''
                               + removeEscape(parseASCII(i['summary'])) + '\',  \''
                               + removeEscape(parseASCII(i['description']['text'])) + '\', \''
                               + removeEscape(i['url']) + '\', \''
                               + i['start']['local'] + '\', \''
                               + i['end']['local'] + '\', \''
                               + i['changed'][0: i['published'].find('Z')] + '\',  \''
                               + i['status'] + '\', \''
                               + str(i['online_event']) + '\', \''
                               + datetime.now().strftime('%m/%d/%Y %H:%M:%S') + '\', \''
                               + stringCategory + '\', \''
                               + removeEscape(parseASCII(i['venue']['address']['localized_address_display'])) + '\')')
                conn.commit()
            print('Eventbrite page parsed: ' + category + ' page ' + str(pageNumber))


scrapeEventbrite()

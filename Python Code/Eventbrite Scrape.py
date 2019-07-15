import requests
import string
import pyodbc


# Connecting to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=jackson;'
                      'Database=OppHunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


def removeEscape(text):
    return text.replace('\'', '\'\'')

def parseASCII(text):
    if(text is not None):
        return ''.join(filter(lambda x: x in string.printable, text))
    else:
        return ''


pageNumParam = {"categories": "101", "location.address": "NewYork",
              "location.within": "8mi", "token": "4DYO5EC3JABSP5NVOGOX"}
pageNumRequest = requests.get('https://www.eventbriteapi.com/v3/events/search',
                              pageNumParam)
pagenumJSON = pageNumRequest.json()

numPages = int(pagenumJSON['pagination']['page_count'])
for pageNumber in range(1, numPages):
    eventParam = {"categories": "101", "location.address": "NewYork",
                  "location.within": "8mi", "expand": "venue",
                  "page": pageNumber, "token": "4DYO5EC3JABSP5NVOGOX"}
    eventRequest = requests.get('https://www.eventbriteapi.com/v3/events/search',
                                eventParam)
    eventJSON = eventRequest.json()
    for i in eventJSON['events']:
        cursor.execute('INSERT into eventBrite_raw (Title, shortSummary, longSummary, '
                       + 'URL, eventStart, eventEnd, publishDate, status, onlineEvent, address) VALUES (\''
                       + removeEscape(parseASCII(i['name']['text'])) + '\', \''
                       + removeEscape(parseASCII(i['summary'])) + '\',  \''
                       + removeEscape(parseASCII(i['description']['text'])) + '\', \''
                       + removeEscape(i['url']) + '\', \''
                       + removeEscape(i['start']['local']) + '\', \''
                       + removeEscape(i['end']['local']) + '\', \''
                       + removeEscape(i['published'][0: i['published'].find('Z')]) + '\',  \''
                       + removeEscape(i['status']) + '\', \''
                       + removeEscape(str(i['online_event'])) + '\', \''
                       + removeEscape(parseASCII(i['venue']['address']['localized_address_display'])) + '\')')
        conn.commit()
    print('Page parsed: ' + str(pageNumber))

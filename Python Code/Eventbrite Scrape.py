import requests
import string

eventParam = {"categories": "101", "location.address": "NewYork",
              "location.within": "8mi", "expand": "venue",
              "page": "48", "token": "4DYO5EC3JABSP5NVOGOX"}
eventRequest = requests.get('https://www.eventbriteapi.com/v3/events/search',
                            eventParam)
print(eventRequest.status_code)
eventJSON = eventRequest.json()
print(eventRequest.text)
for i in eventJSON['events']:
    print(''.join(filter(lambda x: x in string.printable, i['name']['text'])))
    print(''.join(filter(lambda x: x in string.printable, i['summary'])))
    print(''.join(filter(lambda x: x in string.printable, i['description']['text'])))
    print(i['url'])
    print(i['start']['local'])
    print(i['end']['local'])
    print(i['published'][0: i['published'].find('Z')])
    print(i['status'])
    print(i['online_event'])
    print(i['venue']['address']['localized_address_display'])

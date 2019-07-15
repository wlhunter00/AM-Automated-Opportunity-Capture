import requests

request = requests.get('http://api.open-notify.org/astros.json')
print(request.text)

requestJSON = request.json()

print('Number of people in space:', requestJSON['number'])

for person in requestJSON['people']:
    print(person['name'])
print(request.status_code)

rhymeParam = {"rel_rhy": "jingle"}
rhymes = requests.get('https://api.datamuse.com/words', rhymeParam)
rhymeJSON = rhymes.json()

print(rhymeJSON)
for i in rhymeJSON[0:3]:
    print(i['word'])

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

descriptions = []
agencies = []
issue_dates = []
due_dates = []
locations = []
categories = []
ad_type = []

url = 'https://www.nyscr.ny.gov/adsOpen.cfm?startnum=1&orderBy=55&numPer=50&myAdsOnly=2&adClass=b&adCat=&adCounty=&adType=&mbe=0&wbe=0&dbe=0&keyword='
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

job_containers = soup.findAll('tr', class_='r1')
# print(type(job_containers))
# print(len(job_containers))

for container in job_containers:
    container_outputs = container.findAll('div', class_="resultText")
    if(len(container_outputs) > 6):
        for num in range(0, len(container_outputs), 1):
            if(num == 0):
                descriptions.append(container_outputs[num].text)
            if(num == 1):
                agencies.append(container_outputs[num].text)
            if(num == 2):
                issue_dates.append(container_outputs[num].text)
            if(num == 3):
                due_dates.append(container_outputs[num].text)
            if(num == 4):
                locations.append(container_outputs[num].text)
            if(num == 5):
                categories.append(container_outputs[num].text)
            if(num == 6):
                ad_type.append(container_outputs[num].text)
print(len(categories))
for num in range(0, len(categories)):
    print(descriptions[num])
    print(agencies[num])
    print(issue_dates[num])
    print(due_dates[num])
    print(locations[num])
    print(categories[num])
    print(ad_type[num])

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# 20 jobs per pages
# 50 pages

# connecting to website

url = 'https://www.contractsfinder.service.gov.uk/Search/Results?&page=1#dashboard_notices'
response = requests.get(url)

# Finding all of the hyperlink HTML tags

soup = BeautifulSoup(response.text, "html.parser")
containers = soup.findAll('div', class_='search-result')
# print(soup.prettify)
# print(containers[1])

# Title (url is in here too)
title = containers[19].find('div', class_='search-result-header')
link = title.find('a')['href']
# print(title.text)
# print(link)

description = containers[0].find('span', class_='')
print(description)

company = containers[1].find('div', class_='search-result-sub-header wrap-text')

label = []
result = []
# result = containers[1].findAll('strong', class_='fieldValue')
test = containers[1].findAll('div', class_='search-result-entry')
for yeet in test:
    label.append(yeet.find('strong', class_='').text)
    result.append(yeet.find('strong', class_='').next_sibling)
# print(label[1], result[1])

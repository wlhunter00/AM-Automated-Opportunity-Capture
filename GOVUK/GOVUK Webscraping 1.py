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
<<<<<<< HEAD
=======

description = containers[0].find('span', class_='')
print(description)
>>>>>>> 8938cf4d645c4eac07f3fcd33fef335c4d5f33ac

company = containers[1].find('div', class_='search-result-sub-header wrap-text')

label = []
result = []
# result = containers[1].findAll('strong', class_='fieldValue')
test = containers[0].findAll('div', class_='search-result-entry')
print(test[0])
for yeet in test:
    label.append(yeet.find('strong', class_='').text)
    print(yeet.find('strong', class_='').text)
    result.append(yeet.find('strong', class_='').next_sibling)
<<<<<<< HEAD
    print(yeet.find('strong', class_='').next_sibling)
# print(label[0])
# print(result[0])
=======
# print(label[1], result[1])
>>>>>>> 8938cf4d645c4eac07f3fcd33fef335c4d5f33ac

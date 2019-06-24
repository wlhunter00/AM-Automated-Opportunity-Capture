import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# connecting to website

url = 'https://www.dasny.org/opportunities/rfps-bids?field_solicitation_classificatio_target_id=All&field_solicitation_type_target_id=All&field_goals_target_id=All&field_set_aside_target_id=All&query=&page=0'
response = requests.get(url)

# Finding all of the hyperlink HTML tags

soup = BeautifulSoup(response.text, "html.parser")
containers = soup.findAll('div', class_='views-row')
print(soup.prettify)
# print(containers[1])

# Title (url is in here too)
<<<<<<< HEAD
title = containers[1].findAll('div', class_='rfp-bid-title')
link = 'https://www.dasny.org' + title[0].find('a')['href']
# print(link)
=======
title = containers[1].find('div', class_='rfp-bid-title')
link = 'https://www.dasny.org' + title.find('a')['href']
print(title.text)
>>>>>>> 9ee7a0232c0c6890e1c7f9badf24a3a15a80c2cd

result = containers[1].findAll('td', class_='fieldValue')
label = containers[1].findAll('td', class_='')
# print(result[1].text)
# for test in info:
#     print(test.prettify)

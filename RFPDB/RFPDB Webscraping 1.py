import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# 20 jobs per pages
# 50 pages

# connecting to website

url = 'http://www.rfpdb.com/view/category/name/technology/page/1'
response = requests.get(url)

# Finding all of the hyperlink HTML tags

soup = BeautifulSoup(response.text, "html.parser")
containers = soup.findAll('li', class_='approved imported current soon schema')
# print(soup.prettify)
# print(containers[1])

title = containers[1].find('a')
link = containers[1].find('a')['href']
description = containers[1].find('a')['itemprop']
print(title.text)
print(link)
# Title (url is in here too)
# title = containers[19].find('div', class_='search-result-header')
# link = title.find('a')['href']
# # print(title.text)
# # print(link)
#
# description = containers[0].find('span', class_='')
# print(description)
#
# company = containers[1].find('div', class_='search-result-sub-header wrap-text')
#
# label = []
# result = []
# # result = containers[1].findAll('strong', class_='fieldValue')
# test = containers[0].findAll('div', class_='search-result-entry')
# print(test[0])
# for yeet in test:
#     label.append(yeet.find('strong', class_='').text)
#     print(yeet.find('strong', class_='').text)
#     result.append(yeet.find('strong', class_='').next_sibling)

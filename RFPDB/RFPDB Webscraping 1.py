import requests
from bs4 import BeautifulSoup

# 20 jobs per pages
# 50 pages

# connecting to website

url = 'http://www.rfpdb.com/view/category/name/analysis/page/1'
response = requests.get(url)

# Finding all of the hyperlink HTML tags

soup = BeautifulSoup(response.text, "html.parser")
containers = soup.select('li[itemtype="http://schema.org/CreativeWork/RequestForProposal"]')
# print(containers[0])

labels = []
results = []
labels.append(containers[0].find('a')['itemprop'])
results.append('http://www.rfpdb.com'+containers[0].find('a')['href'])
labels.append('title')
results.append(containers[0].find('a').text)
labels.append(containers[0].find('span', class_='comment')['itemprop'])
results.append(containers[0].find('span', class_='comment').text)
labels.append(containers[0].find('time')['itemprop'])
results.append(containers[0].find('time')['datetime'])
labels.append('Location')
results.append(containers[0].select_one('span[itemprop="address"]').text)
labels.append('Categories')
results.append(containers[0].find('ul', class_='categories').text)


for num in range(0, len(labels)):
    print(labels[num] + ': ' + results[num])

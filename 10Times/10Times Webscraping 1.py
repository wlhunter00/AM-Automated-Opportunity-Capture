import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
# 20 jobs per pages
# 50 pages

# connecting to website
# url = 'https://10times.com/newyork-us'
# response = requests.get(url)

# I used Firefox; you can use whichever browser you like.
browser = webdriver.Chrome(executable_path=r'C:\\Users\\whunter\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe')
browser.get('https://10times.com/newyork-us/tradeshows')

# Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False
while(not match):
    lastCount = lenOfPage
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(3)
    print('test')
    if (lastCount == lenOfPage):
        print('end of page')
        match = True
print('scrolling done')
# Now that the page is fully scrolled, grab the source code.
source_data = browser.page_source
print('yeet')
print(source_data.encode("utf-8"))
soup = BeautifulSoup(source_data, "html.parser")
print(soup.prettify())
browser.quit()
print('cool')
# print(type(bs_data))
# soup = BeautifulSoup(response.text, "html.parser")
# print(soup)
# containers = soup.select('li[itemtype="http://schema.org/CreativeWork/RequestForProposal"]')
# # print(containers[0])
#
# labels = []
# results = []
# labels.append(containers[0].find('a')['itemprop'])
# results.append('http://www.rfpdb.com'+containers[0].find('a')['href'])
# labels.append('title')
# results.append(containers[0].find('a').text)
# labels.append(containers[0].find('span', class_='comment')['itemprop'])
# results.append(containers[0].find('span', class_='comment').text)
# labels.append(containers[0].find('time')['itemprop'])
# results.append(containers[0].find('time')['datetime'])
# labels.append('Location')
# results.append(containers[0].select_one('span[itemprop="address"]').text)
# labels.append('Categories')
# results.append(containers[0].find('ul', class_='categories').text)
#
#
# for num in range(0, len(labels)):
#     print(labels[num] + ': ' + results[num])

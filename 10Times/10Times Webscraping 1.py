import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
# 20 jobs per pages
# 50 pages

# connecting to website
url = 'https://10times.com/newyork-us/technology'
response = requests.get(url)


def infiniteScroll(url, endElement, endCSS):
    browser = webdriver.Chrome(executable_path=r'C:\\Users\\wlhun\\Downloads\\chromedriver_win32\\chromedriver.exe')
    browser.get(url)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(not match):
        lastCount = lenOfPage
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(3)
        displayed = browser.find_element_by_id(endElement).value_of_css_property(endCSS)
        if ((lastCount == lenOfPage) and (displayed != 'block')):
            print('end of page')
            match = True
    print('scrolling done')
    code = browser.page_source
    browser.quit()
    return code


source_data = infiniteScroll('https://10times.com/newyork-us/technology', 'ajax', 'display')
# soup = BeautifulSoup(response.text, "html.parser")
soup = BeautifulSoup(source_data, "html.parser")

# Categories: technology, business-consultancy, finance
# Job object: <tr class="box">

jobs = soup.findAll('tr', class_='box')


def parseAds(jobContainer, requiredHTML, requiredClass):
    for job in jobContainer:
        title = job.find(requiredHTML, class_=requiredClass)
        if not title:
            jobs.remove(job)
            continue
    return jobContainer


jobs = parseAds(jobs, 'td', 'text-drkr')

for job in jobs:
    timing = job.find('td', class_='text-drkr')
    # print(timing.text)
    # print(timing)
    # print(len(list(timing.children)))
    print(timing.contents)
    title = job.find('h2')
    URL = title.find('a')['href']
    location = job.find('span', class_='venue text-drkr')
    # description = location.next_sibling()
    # print(description.text)

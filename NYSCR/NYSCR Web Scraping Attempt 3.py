# Important imports
import requests
import time
from bs4 import BeautifulSoup
import pyodbc
# Create arrays to store the data. Try to collect as much as possible from the
# website, and see what fits into the SQL schema
descriptions = []
agencies = []
issue_dates = []
due_dates = []
locations = []
categories = []
ad_type = []
listing_number = []
# Connecting to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=US-NYC-NL000860\SQLEXPRESS;'
                      'Database=Opportunity Hunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
# Keeping track of the page we are scraping
pageNumber = 1
# 1 and 50 are the pages we want to start at. str() casts these as strings
startNum = [str(1), str(50)]
# For loop that goes through the array. Basically allows us to run multiple
# pages
for start in startNum:
    # You want the URL to be very specific. Apply the filters on the site to
    # get the exact url that you want. Insert the start which is the string we
    # set above.
    url = 'https://www.nyscr.ny.gov/adsOpen.cfm?startnum=' + start + '&orderBy=55&numPer=50&myAdsOnly=2&adClass=b&adCat=&adCounty=&adType=&mbe=0&wbe=0&dbe=0&keyword='
    # Just connecting to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # The job_containers is the HTML element that encompases every job. Allows
    # us to run multiple containers
    job_containers = soup.findAll('tr', class_='r1')
    # A for loop that goes through all of the containers and extracts the info
    # from the specific job. The way this is done will differ for each website
    for container in job_containers:
        # Collecting the information from the container
        container_outputs = container.findAll('div', class_="resultText")
        if(len(container_outputs) > 6):
            if(pageNumber == 1):
                listing_number.append(int(container.find('td', class_="c1 tblColor").text))
            if(pageNumber == 2):
                listing_number.append(int(container.find('td', class_="c1 tblColor").text)+49)
            for num in range(0, len(container_outputs), 1):
                # Insert the information into arrays
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
    pageNumber += 1
    # 1 second delay to avoid overtaxing the server
    time.sleep(1)
# Print statements as a debug
print(len(categories))
for num in range(0, len(categories)):
    print(listing_number[num])
    print(descriptions[num])
    cursor.execute('INSERT into NYSCRpythonCleaned (jobDescription) VALUES (\''
        + descriptions[num].replace('\'','\'\'') + '\')')
    conn.commit()
    print(agencies[num])
    print(issue_dates[num])
    cursor.execute('INSERT into NYSCRpythonCleaned (issueDateTest) VALUES (\''
        + issue_dates[num] + '\')')
    conn.commit()
    print(due_dates[num])
    print(locations[num])
    print(categories[num])
    print(ad_type[num])

# Important imports
import requests
import time
from bs4 import BeautifulSoup
import pyodbc
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
        # Print statement as debug
        print(container)
        # Insert text block plus URL into SQL table
        # cursor.execute('INSERT into NYSCRuncleaned (BodyText, HTML) VALUES (\''
        #        + container.text.replace('\'','\'\'') + ' URL:' + url + '\'),\''
                # + container.prettify().replace('\'','\'\'') + '   URL:' + url + '\') ')
        cursor.execute('INSERT into NYSCRuncleaned (BodyText) VALUES (\''
                + container.prettify().replace('\'','\'\'') + '   URL:' + url + '\')')
        conn.commit()
    pageNumber += 1
    # 1 second delay to avoid overtaxing the server
    time.sleep(1)

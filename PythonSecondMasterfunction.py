# Imports
import yagmail
import pandas as pd
import pyodbc
from datetime import datetime
import glob
import os

# Connecting to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=jackson;'
                      'Database=OppHunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
# Opening file with the keywords. Way these are written is Query:SheetName
keywordFile = open("C:/Users/whunter/Documents/GitHub/AM-Automated-Oppurtinity-Capture/SQL-Python Keywords Queries.txt", "r")
lines = keywordFile.readlines()
# Creation of Lists to be Used Later
queries = []
sheets = []
dataFrames = []
dfForCount = []


# Function that goes through text file and stores queries and sheets into
# seperate lists.
def splitKeyWordFile():
    for line in lines:
        splitList = line.split(':')
        queries.append(splitList[0])
        sheets.append(splitList[1])


# Creates data frames from the queries that we gave it and stores these in list
def loadDataFrames():
    for query in queries:
        dataFrames.append(pd.read_sql_query(query, conn))


# For the queries that use LIKE creates dataframes that isolate the new ones so
# we can count the new jobs.
def loadCountingFrames():
    for num in range(3, len(dataFrames)):
        dfForCount.append(dataFrames[num][dataFrames[num]['Status'] == 'New'])


# Given a writer, turns all of the data frames into the excel spreadsheet with
# the name of sheetnames stored from the text file
def writeToExcel(writer):
    for num in range(0, len(dataFrames)):
        dataFrames[num].to_excel(writer, sheet_name=sheets[num])
        print('Loaded: ' + sheets[num])


# Master function for storing in Excel Sheet
def queryToExcelSheet():
    splitKeyWordFile()
    loadDataFrames()
    loadCountingFrames()
    with pd.ExcelWriter(r'C:\Users\whunter\Documents\GitHub\AM-Automated'
                        + '-Oppurtinity-Capture\Excel Sheets\Results_'
                        + datetime.now().strftime('%m-%d-%Y#%H%M')
                        + '.xlsx') as writer:
        writeToExcel(writer)

    with pd.ExcelWriter(r'C:\Users\whunter\Box\OppHunter\OppHunterResults.xlsx') as writer:
        writeToExcel(writer)


# One function to send email
def sendEmail():
    # Opening Local Email Text File to retrieve information. Then stores
    # sensative information in variables.

    file = open("C:/Users/whunter/Documents/Email Information.txt", "r")
    lines = file.readlines()
    senderEmail = lines[1]
    password = lines[3]
    listAddresses = lines[4:]
    list_of_reports = glob.glob(r'C:\Users\whunter\Documents\GitHub\AM-Automated'
                                + '-Oppurtinity-Capture\Excel Sheets\*')
    latest_report = max(list_of_reports, key=os.path.getctime)
    subject = 'Opportunity Hunter Daily Update'
    # Stores string variables to be used in email.
    subject = 'Opportunity Hunter Daily Update'
    body = 'Hello,\n\nThis is the daily Opportunity Hunter Report. Click the link to access the Excel Report.'
    # HTML code for the email, str(dataFrame[X].count(axis=0)[0]) is the count
    # of the rows in each table.
    html = ('<br><a href="https://alvarezandmarsal.box.com/s/hpchnqin29htdjpv0af8oyseilxl6vqc">Opportunity Hunter Report</a><br><br>' +
            '<p>Consider the table below for a quick update of the status of the table. <br>' +
            'Please respond to this email if you have any issues, or want to add any keywords. Please do not leave the table open for too long, as it needs to be closed everywhere for it to be updated.</p>' +
            '<table><tr><th></th><th>Newly Added</th><th>Current Table<th>Master Table</th><th>Data Related</th><th>Tech Related</th><th>Law Related</th><th>Finance Related</th></tr>' +
            '<tr><td>New Additions</td><td align="center">'
            + str(dataFrames[0].count(axis=0)[0])
            + '</td><td align="center">' + str(dataFrames[0].count(axis=0)[0])
            + '</td><td align="center">' + str(dataFrames[0].count(axis=0)[0])
            + '</td><td align="center">' + str(dfForCount[0].count(axis=0)[0])
            + '</td><td align="center">' + str(dfForCount[1].count(axis=0)[0])
            + '</td><td align="center">' + str(dfForCount[2].count(axis=0)[0])
            + '</td><td align="center">' + str(dfForCount[3].count(axis=0)[0])
            + '</td></tr>' + '<tr><td>Total Jobs</td><td align="center">'
            + str(dataFrames[0].count(axis=0)[0])
            + '</td><td align="center">' + str(dataFrames[1].count(axis=0)[0])
            + '</td><td align="center">' + str(dataFrames[2].count(axis=0)[0])
            + '</td><td align="center">' + str(dataFrames[3].count(axis=0)[0])
            + '</td><td align="center">' + str(dataFrames[4].count(axis=0)[0])
            + '</td><td align="center">' + str(dataFrames[5].count(axis=0)[0])
            + '</td><td align="center">' + str(dataFrames[6].count(axis=0)[0])
            + '<br></td></tr></table><p>Thank You.</p>'
            )
    print('Attachments Loaded. Connecting to Server.')
    # Connecting to server
    yag = yagmail.SMTP(senderEmail, password)
    # Sends email.
    yag.send(to=listAddresses, subject=subject, contents=[body, html, latest_report])
    print('Email Sent.')


queryToExcelSheet()
sendEmail()

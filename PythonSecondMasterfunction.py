# Imports
import yagmail
import pandas as pd
import pyodbc
from datetime import datetime

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
    for num in range(3, len(dataFrames)-1):
        dfForCount.append(dataFrames[num][dataFrames[num]['Status'] == 'New'])


# Given a writer, turns all of the data frames into the excel spreadsheet with
# the name of sheetnames stored from the text file
def writeToExcel(writer):
    for num in range(0, len(dataFrames)-1):
        dataFrames[num].to_excel(writer, sheet_name=sheets[num])


# Master function for storing in Excel Sheet
def queryToExcelSheet():
    splitKeyWordFile()
    loadDataFrames()
    loadCountingFrames()
    with pd.ExcelWriter(r'C:\Users\whunter\Documents\GitHub\AM-Automated' +
                         '-Oppurtinity-Capture\Excel Sheets\Results_' +
                          datetime.now().strftime('%m-%d-%Y#%H%M') +
                          '.xlsx') as writer:
        writeToExcel(writer)

    with pd.ExcelWriter(r'C:\Users\whunter\Box\OppHunter\OppHunterResults.xlsx') as writer:
        writeToExcel(writer)
    print(dataFrames[0].count(axis=0)[0])
    print(dfForCount[0].count(axis=0)[0])


# One function to send email
def sendEmail():
    # Opening Local Email Text File to retrieve information. Then stores sensative
    # information in variables.
    EmailInformationfile = open("C:/Users/whunter/Documents/Email Information.txt", "r")
    EmailInformationlines = EmailInformationfile.readlines()
    senderEmail = EmailInformationlines[1]
    password = EmailInformationlines[3]
    listAddresses = EmailInformationlines[4:]

    # Stores string variables to be used in email.
    subject = 'Opportunity Hunter Daily Update'
    body = 'Hello,\n\nThis is the daily Opportunity Hunter Report. Click the link to access the Excel Report.'
    html = ('<br><a href="https://alvarezandmarsal.box.com/s/hpchnqin29htdjpv0af8oyseilxl6vqc">Opportunity Hunter Report</a><br><br>' +
            '<p>Consider the table below for a quick update of the status of the table. <br>' +
            'Please respond to this email if you have any issues, or want to add any keywords. Please do not leave the table open for too long, as it needs to be closed everywhere for it to be updated.</p>' +
            '<table><tr><th></th><th>Newly Added</th><th>Current Table<th>Master Table</th><th>Data Related</th><th>Tech Related</th><th>Law Related</th><th>Finance Related</th></tr>' +
            '<tr><td>New Additions</td><td align="center">' + dataFrames[0].count(axis=0)[0] +
            '</td><td align="center">' + dataFrames[0].count(axis=0)[0] + '</td><td align="center">' + dataFrames[0].count(axis=0)[0] +
            '</td><td align="center">' + dfForCount[0].count(axis=0)[0] + '</td><td align="center">' + dfForCount[1].count(axis=0)[0] +
            '</td><td align="center">' + dfForCount[2].count(axis=0)[0] + '</td><td align="center">' + dfForCount[3].count(axis=0)[0] +
            '</td></tr>' + '<tr><td>Total Jobs</td><td align="center">' + dataFrames[0].count(axis=0)[0] +
            '</td><td align="center">' + dataFrames[1].count(axis=0)[0] + '</td><td align="center">' + dataFrames[2].count(axis=0)[0] +
            '</td><td align="center">' + dataFrames[3].count(axis=0)[0] + '</td><td align="center">' + dataFrames[4].count(axis=0)[0] +
            '</td><td align="center">' + dataFrames[5].count(axis=0)[0] + '</td><td align="center">' + dataFrames[6].count(axis=0)[0] +
            '<br></td></tr></table><p>Thank You.</p>'
            )
    # connects to server and sends email.
    yag = yagmail.SMTP(senderEmail, password)
    yag.send(to=listAddresses, subject=subject, contents=[body, html])


sendEmail()
queryToExcelSheet()

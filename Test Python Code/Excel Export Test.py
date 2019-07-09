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


queryToExcelSheet()

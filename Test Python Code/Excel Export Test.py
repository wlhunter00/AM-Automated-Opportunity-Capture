import pandas as pd
import pyodbc
from datetime import datetime

# Connecting to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=jackson;'
                      'Database=OppHunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

keywordFile = open("C:/Users/whunter/Documents/GitHub/AM-Automated-Oppurtinity-Capture/SQL-Python Keywords Queries.txt", "r")
lines = keywordFile.readlines()
queries = []
sheets = []
dataFrames = []
dfForCount = []
queryToSheets = []


class queryToSheet:
    def __init__(self, query, sheetName):
        self.query = query
        self.sheetName = sheetName

    def createDataFrame(self, masterObject):
        self.df = pd.read_sql_query(self.query, conn)
        self.totalJobs = self.df.count(axis=0)[0]
        if(self.sheetName != "master_table"):
            self.newJobs = self.df[self.df['Status'] == 'New'].count(axis=0)[0]
        else:
            self.newJobs = masterObject.df.count(axis=0)[0]


def testMethod(writer):
    for num in range(0, len(sheets)-1):
        queryToSheets.append(queryToSheet(queries[num], sheets[num]))
        if(num == 0):
            queryToSheets[num].createDataFrame("")
        else:
            queryToSheets[num].createDataFrame(queryToSheet[1])
        queryToSheet[num].df.to_excel(writer, sheet_name=queryToSheet[num].sheetName)

#
# def returnDataFrame(script):
#     return pd.read_sql_query(script, conn)
#
#
# def loadDataFrames():
#     for query in queries:
#         dataFrames.append(returnDataFrame(query))
#
#
# def loadCountingFrames():
#     for num in range(3, len(dataFrames)-1):
#         dfForCount.append(dataFrames[num][dataFrames[num]['Status'] == 'New'])
#
#
# def writeToExcel():
#     for num in range(0, len(dataFrames)-1):
#         dataFrames[num].to_excel(writer, sheet_name=sheets[num])


for line in lines:
    splitList = line.split(':')
    queries.append(splitList[0])
    sheets.append(splitList[1])

#
# loadDataFrames()
# loadCountingFrames()
#
# print(dataFrames[0].count(axis=0)[0])
# print(dfForCount[0].count(axis=0)[0])


with pd.ExcelWriter(r'C:\Users\whunter\Documents\GitHub\AM-Automated' +
                     '-Oppurtinity-Capture\Excel Sheets\Results_' +
                      datetime.now().strftime('%m-%d-%Y#%H%M') +
                      '.xlsx') as writer:
    # writeToExcel()
    testMethod(writer)

with pd.ExcelWriter(r'C:\Users\whunter\Box\OppHunter\OppHunterResults.xlsx') as writer:
    # writeToExcel()
    testMethod(excel)

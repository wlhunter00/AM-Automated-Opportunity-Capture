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
for line in lines:
    splitList = line.split(':')
    queries.append(splitList[0])
    sheets.append(splitList[1])


def returnDataFrame(script):
    return pd.read_sql_query(script, conn)


def loadDataFrames():
    for query in queries:
        dataFrames.append(returnDataFrame(query))


def loadCountingFrames():
    for num in range(3, len(dataFrames)-1):
        dfForCount.append(dataFrames[num][dataFrames[num]['Status'] == 'New'])


loadDataFrames()
loadCountingFrames()

print(dataFrames[0].count(axis = 0)[0])
print(dfForCount[0].count(axis = 0)[0])

def writeToExcel():
    for num in range(0, len(dataFrames)-1):
        dataFrames[num].to_excel(writer, sheet_name=sheets[num])

with pd.ExcelWriter(r'C:\Users\whunter\Documents\GitHub\AM-Automated' +
                     '-Oppurtinity-Capture\Excel Sheets\Results_' +
                      datetime.now().strftime('%m-%d-%Y#%H%M') +
                      '.xlsx') as writer:
    writeToExcel()

with pd.ExcelWriter(r'C:\Users\whunter\Box\OppHunter\OppHunterResults.xlsx') as writer:
    writeToExcel()

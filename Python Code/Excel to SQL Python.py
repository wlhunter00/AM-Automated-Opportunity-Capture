import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=jackson;'
                      'Database=OppHunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

df = pd.read_excel("C:\\Users\\whunter\\Documents\\GitHub\\AM-Automated-Oppurtinity-Capture\\DI Projects_Description & Fees_7.9.19.xlsx")
# cursor.execute('create table jobDescriptions_tbl(pay int, description nvarchar(max))')
# conn.commit()
for num in range(0, len(df.index)-1):
    try:
        cursor.execute("INSERT into jobDescriptions_tbl (pay, description) VALUES ("
                       + str(df.loc[num][0]) + ", '" + df.loc[num][1].replace("'", "") + "')")
        conn.commit()
    except:
        print("INSERT into jobDescriptions_tbl (pay, description) VALUES ("
                       + str(df.loc[num][0]) + ", '" + df.loc[num][1].replace("'", "") + "')")

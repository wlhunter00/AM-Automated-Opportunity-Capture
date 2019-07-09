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


script1 = "select * from current_table where status = 'new'"
df1 = pd.read_sql_query(script1, conn)

script2 = 'select * from current_table'
df2 = pd.read_sql_query(script2, conn)

script3 = 'select * from master_table'
df3 = pd.read_sql_query(script3, conn)

script4 = "select * from current_table where JobDescription like '%data%'"
df4 = pd.read_sql_query(script4, conn)

script5 = "select * from current_table where JobDescription like '%tech%'"
df5 = pd.read_sql_query(script5, conn)

script6 = "select * from current_table where JobDescription like '%legal%' or JobDescription like '%law%'"
df6 = pd.read_sql_query(script6, conn)

script7 = "select * from current_table where JobDescription like '%financ%'"
df7 = pd.read_sql_query(script7, conn)

print(df7)

#
# with pd.ExcelWriter(r'C:\Users\whunter\Documents\GitHub\AM-Automated' +
#                      '-Oppurtinity-Capture\Excel Sheets\Results_' +
#                       datetime.now().strftime('%m-%d-%Y#%H%M') +
#                       '.xlsx') as writer:
#     df1.to_excel(writer, sheet_name='newly_added')
#     df2.to_excel(writer, sheet_name='current_table')
#     df3.to_excel(writer, sheet_name='master_table')
#     df4.to_excel(writer, sheet_name='data_related')
#     df5.to_excel(writer, sheet_name='tech_related')
#     df6.to_excel(writer, sheet_name='legal_related')
#     df7.to_excel(writer, sheet_name='finance_related')
#
# with pd.ExcelWriter(r'C:\Users\whunter\Box\OppHunter\OppHunterResults.xlsx') as writer:
#     df1.to_excel(writer, sheet_name='newly_added')
#     df2.to_excel(writer, sheet_name='current_table')
#     df3.to_excel(writer, sheet_name='master_table')
#     df4.to_excel(writer, sheet_name='data_related')
#     df5.to_excel(writer, sheet_name='tech_related')
#     df6.to_excel(writer, sheet_name='legal_related')
#     df7.to_excel(writer, sheet_name='finance_related')



list_of_files = glob.glob(r'C:\Users\whunter\Documents\GitHub\AM-Automated' +
                           '-Oppurtinity-Capture\Excel Sheets\*')
latest_file = max(list_of_files, key=os.path.getctime)
print(str(latest_file))

# Important imports
import pyodbc
from sqlite3 import OperationalError
# Connecting to SQL server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=jackson;'
                      'Database=OppHunter;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
            conn.commit()
            print(str(command) + " excecuted.")
        except OperationalError:
            print("Command skipped: " + str(command))


executeScriptsFromFile(
    "C:\\Users\\whunter\\Documents\\GitHub\\AM-Automated-Oppurtinity-Capture\\SQL Scripts\\Master Function Query.sql")
cursor.close()
conn.close()
print('All sites scraped')

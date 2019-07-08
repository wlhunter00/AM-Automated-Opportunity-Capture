import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import glob
import os

port = 465  # For SSL

file = open("C:/Users/whunter/Desktop/Email Information.txt", "r")
lines = file.readlines()
senderEmail = lines[1]
password = lines[3]
listAddresses = lines[4:]

list_of_files = glob.glob(r'C:\Users\whunter\Documents\GitHub\AM-Automated' +
                           '-Oppurtinity-Capture\Excel Sheets\*')
latest_file = max(list_of_files, key=os.path.getctime)

for i in range(len(listAddresses)):
    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = listAddresses[i]
    msg['Subject'] = "Opportunity Hunter Daily Update"
    body = "This is a test."
    msg.attach(MIMEText(body, 'plain'))
    filename = "Results.xlsx"
    attachment = open(latest_file, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(senderEmail, password)
    text = msg.as_string()
    s.sendmail("sender_email_id", listAddresses[i], text)
    s.quit()

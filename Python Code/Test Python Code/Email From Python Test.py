import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL

file = open("C:/Users/whunter/Desktop/Email Information.txt", "r")
lines = file.readlines()
senderEmail = lines[1]
password = lines[3]
listAddresses = lines[4:]

for i in range(len(listAddresses)):
    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = listAddresses[i]
    msg['Subject'] = "Opportunity Hunter Daily Update"
    body = "Test Round Four."
    html = """\
    <html>
      <body>
        <p>Hi All,<br><br>
           This is the daily Opportunity Hunter Report. Click the link to access the Excel Report.<br><br>
           <a href="https://alvarezandmarsal.box.com/s/hpchnqin29htdjpv0af8oyseilxl6vqc">Opportunity Hunter Report</a><br><br>
           Consider the table below for a quick update of the status of the table. <br>
           Please respond to this email if you have any issues, or want to add any keywords.
        </p>
        <table>
          <tr>
            <th></th>
            <th>Newly Added</th>
            <th>Current Table</th>
            <th>Master Table</th>
            <th>Data Related</th>
            <th>Tech Related</th>
            <th>Law Related</th>
            <th>Finance Related</th>
          </tr>
          <tr>
            <td>New Additions</td>
            <td>A</td>
            <td>B</td>
            <td>C</td>
            <td>D</td>
            <td>E</td>
            <td>F</td>
            <td>G</td>
          </tr>
          <tr>
            <td>Total Jobs</td>
            <td>H</td>
            <td>I</td>
            <td>J</td>
            <td>K</td>
            <td>L</td>
            <td>M</td>
            <td>N<br></td>
          </tr>
        </table>
        <p>
          Thank You.
        </p>
      </body>
    </html>
    """
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(senderEmail, password)
    text = msg.as_string()
    s.sendmail("sender_email_id", listAddresses[i], text)
    s.quit()

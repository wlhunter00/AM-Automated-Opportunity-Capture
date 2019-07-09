import yagmail

file = open("C:/Users/whunter/Desktop/Email Information.txt", "r")
lines = file.readlines()
senderEmail = lines[1]
password = lines[3]
listAddresses = lines[4:]
subject = 'Opportunity Hunter Daily Update'
test = 'x'

yag = yagmail.SMTP(senderEmail, password)

body = 'Hello,\n\nThis is the daily Opportunity Hunter Report. Click the link to access the Excel Report.'
html = ('<br><a href="https://alvarezandmarsal.box.com/s/hpchnqin29htdjpv0af8oyseilxl6vqc">Opportunity Hunter Report</a><br><br>' +
        '<p>Consider the table below for a quick update of the status of the table. <br>' +
        'Please respond to this email if you have any issues, or want to add any keywords. Please do not leave the table open for too long, as it needs to be closed everywhere for it to be updated.</p>' +
        '<table><tr><th></th><th>Newly Added</th><th>Current Table<th>Master Table</th><th>Data Related</th><th>Tech Related</th><th>Law Related</th><th>Finance Related</th></tr>' +
        '<tr><td>New Additions</td><td align="center">' + test +
        '</td><td align="center">' + test + '</td><td align="center">' + test +
        '</td><td align="center">' + test + '</td><td align="center">' + test +
        '</td><td align="center">' + test + '</td><td align="center">' + test +
        '</td></tr>' + '<tr><td>Total Jobs</td><td align="center">' + test +
        '</td><td align="center">' + test + '</td><td align="center">' + test +
        '</td><td align="center">' + test + '</td><td align="center">' + test +
        '</td><td align="center">' + test + '</td><td align="center">' + test +
        '<br></td></tr></table><p>Thank You.</p>'
        )

yag.send(to=listAddresses, subject=subject, contents=[body, html])

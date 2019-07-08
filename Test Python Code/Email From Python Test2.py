import yagmail

receiver = "wlhunter00@gmail.com"
body = "Hello there from Yagmail"
filename = "document.pdf"
subject = "test"
yag = yagmail.SMTP("amopportunityhunter@gmail.com")
yag.send(to=receiver, subject=subject, contents=body, attachments=None)

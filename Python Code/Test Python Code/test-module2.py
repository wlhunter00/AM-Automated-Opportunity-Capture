import string

test = "Crear unaidea de negocio que funcione"


def parseASCII(text):
    if(text is not None):
        return ''.join(filter(lambda x: x in string.printable, text)).replace('', '')
    else:
        return ''


print(parseASCII(test))
for num in range(6, 8):
    print(num)

yeet1 = "right here"
yeet2 = "test"
yeet = """this {0} is a {1} double string test: {0}{1} string \
yeet yeet YEET""".format(yeet1, yeet2)

print(yeet)

bodyParagraph = ('<br><a href="https://alvarezandmarsal.box.com/s/hpchn'
                 'qin29htdjpv0af8oyseilxl6vqc">Opportunity Hunter '
                 'Report</a><br><br><p>Consider the table below for a '
                 'quick update of the status of the table. <br>Please '
                 'respond to this email if you have any issues, or want'
                 ' to add any keywords. Please do not leave the table '
                 'open for too long, as it needs to be closed '
                 'everywhere for it to be updated.</p><table><tr><th>'
                 '</th><th>Newly Added Jobs</th><th>Newly Added Events'
                 '</th><th>Jobs Current Table</th><th>Events Current '
                 'Table</th><th>Events Networking Related</th><th>'
                 'Events Data Related</th><th>Jobs Data Related</th>'
                 '<th>Jobs Tech Related</th><th>Jobs Finance Related'
                 '</th></tr><tr><td>New Additions</td><td align="center">')
print(bodyParagraph)

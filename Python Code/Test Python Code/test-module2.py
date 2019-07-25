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
yeet = "this {0} is a {1} string ".format(yeet1, yeet2)

print(yeet)

readMePlug = ('<p>Access the <a href="https://github.com/wlhunter00/AM-Auto'
          'mated-Opportunity-Capture/blob/master/README.md">README'
              '</a><br><br>README for the latest updates on the project</p><br><p>')
print(readMePlug)

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

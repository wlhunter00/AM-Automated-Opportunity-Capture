import math
import datetime
import string

printable = set(string.printable)
print(datetime.datetime.now().strftime("%b %d %Y - %H:%M:%S.%f"))
z = 10

pop = "this is a string"

numbers = [2, 5, 10, 19, 12]
for number in numbers:
    print(number)

for x in range(0, 3):
    print("We are on time %d" % (x) + " test " + str(x))

print(''.join(filter(lambda x: x in string.printable, pop)))



class ABC:
    def method_abc(self):
        print("I am in method_abc of ABC class. ")


class_ref = ABC()  # object of ABC class
class_ref.method_abc()

ceil_val = math.ceil(15.26)
print("The ceiling value of 15.26 is ", ceil_val)


def test_function(yeet):
    print("this is a test function " + str(yeet))
    return 10


print(test_function("hello"))

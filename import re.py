import re

postalCode = input()
print(postalCode)
print(type(postalCode))

regex = re.compile(r'[0-9][0-9]\-[0-9][0-9][0-9]')
if (re.findall(regex, postalCode)):
    print("yes")
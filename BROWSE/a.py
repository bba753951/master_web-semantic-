import os
if os.path.isfile("a.csv"):
    print(1)
else:
    print(2)
with open("a.csv","r")as fp:
    a=fp.read()

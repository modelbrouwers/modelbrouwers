import os

template = open("settings.py_template","r").read()

cd = os.getcwd()
cd = cd.replace("\\","/")
if cd[-1] != "/":
    cd = cd + "/"

template = template.replace("{ CD }",cd)

open("settings.py","w").write(template)

print "settings created"
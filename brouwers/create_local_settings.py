import os

template = open("local_settings.py__template","r").read()

cd = os.getcwd()
cd = cd.replace("\\","/")
if cd[-1] != "/":
    cd = cd + "/"

template = template.replace("{ CD }",cd)

open("local_settings.py","w").write(template)

print "settings created"

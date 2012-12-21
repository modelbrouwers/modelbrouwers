import os

template = open("settings.py_template","r").read()

cd = os.getcwd()
project_dir = os.path.abspath(os.path.join(cd, os.path.pardir))
project_dir = project_dir.replace("\\","/")
if project_dir[-1] != "/":
    project_dir = project_dir + "/"

template = template.replace("{ CD }", project_dir)

open("settings.py","w").write(template)

print "settings created"

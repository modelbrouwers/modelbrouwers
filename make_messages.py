#!/usr/bin/env python
import os

from django.conf import settings

dirs = os.listdir(settings.PROJECT_ROOT)
for app in dirs:
    app_path = os.path.join(settings.PROJECT_ROOT, app)
    locale_path = os.path.join(app_path, "locale")
    if(os.path.exists(locale_path)):
        os.chdir(app_path)
        os.system("../manage.py makemessages -a -e py,txt,html,form")

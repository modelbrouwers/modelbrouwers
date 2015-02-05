"""
WSGI file for Django project. This depends on two environment variables:
  - VIRTUAL_ENV: path to the virtual env for the project
  - DJANGO_SETTINGS_MODULE: the well known settings module

You can specify these envvars as part of the uwsgi task, or let supervisor set
them. Just make sure they exist.
"""


import os
import site
import sys


def setupenv():
    """
    Borrowed and adapted from https://bitbucket.org/maykinmedia/default-project
    """
    # Remember original sys.path.
    prev_sys_path = list(sys.path)

    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv = os.getenv('VIRTUAL_ENV')
    if not os.path.exists(venv):
        sys.exit('Set the VIRTUAL_ENV environment variable')
    os.chdir(venv)
    sys.path = [venv, src_dir] + sys.path

    # find the site-packages within the local virtualenv
    for python_dir in os.listdir('lib'):
        site_packages_dir = os.path.join('lib', python_dir, 'site-packages')
        if os.path.exists(site_packages_dir):
            site.addsitedir(os.path.abspath(site_packages_dir))

    # Reorder sys.path so new directories at the front.
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path

setupenv()

if not os.environ.get('DJANGO_SETTINGS_MODULE', False):
    sys.exit('You need to set the DJANGO_SETTINGS_MODULE environment var')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

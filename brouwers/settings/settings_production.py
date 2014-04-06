from .base import *

try:
    from .secrets import *
except ImportError:
    sys.stderr.write("Create your secrets.py file with the secret settings.")


DEBUG = False
TEMPLATE_DEBUG = False

SESSION_COOKIE_NAME = 'mbsessionid'

from .base import *

try:
    from .secrets import *
except ImportError:
    sys.stderr.write("Create your secrets.py file with the secret settings.")

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'


DEBUG = False
TEMPLATE_DEBUG = False

SESSION_COOKIE_NAME = 'mbsessionid'
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_DOMAIN = '.modelbrouwers.nl'
SESSION_COOKIE_AGE = 60*60*24*7*365 # one year

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'beheer@modelbrouwers.nl'

ALLOWED_HOSTS = ['.modelbrouwers.nl']

try:
    from .local_settings import *
except ImportError:
    pass

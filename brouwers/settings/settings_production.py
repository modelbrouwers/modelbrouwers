import sys

from .base import *

#
# SENTRY
#
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

try:
    from .secrets import *
except ImportError:
    sys.stderr.write("Create your secrets.py file with the secret settings.")

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

DEBUG = False
TEMPLATE_DEBUG = False
DEVELOPMENT = False

#
# SESSION
#
SESSION_COOKIE_DOMAIN = '.modelbrouwers.nl'

#
# EMAIL
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'beheer@modelbrouwers.nl'

#
# SECURITY
#
ALLOWED_HOSTS = ['.modelbrouwers.nl']

#
# COMPRESS
#
COMPRESS_ENABLED = True

import sys

from .base import *

try:
    from .secrets import *
except ImportError:
    sys.stderr.write("Create your secrets.py file with the secret settings.")

#
# DATABASES
#
DATABASES['default']['CONN_MAX_AGE'] = 60 * 15  # a test

#
# STATICFILES
#
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

#
# SESSION
#
SESSION_COOKIE_NAME = 'mb-staging-sessionid'

#
# CACHE
#
CACHES['default']['KEY_PREFIX'] = 'staging'

#
# SENTRY
#
INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

ALLOWED_HOSTS = ['staging.modelbrouwers.nl', '192.168.1.10']

#
# TEMPLATES
#
TEMPLATES[0]['APP_DIRS'] = False  # conflicts with explicitly specifying the loaders
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', RAW_TEMPLATE_LOADERS),
]

#
# SECURITY
#
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60  # start really low

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SHOP_ENABLED = True

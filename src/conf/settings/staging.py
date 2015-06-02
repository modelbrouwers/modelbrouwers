import sys

from .base import *

try:
    from .secrets import *
except ImportError:
    sys.stderr.write("Create your secrets.py file with the secret settings.")

#
# DATABASES
#
DATABASES['default']['CONN_MAX_AGE'] = 60*15  # a test

#
# STATICFILES
#
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

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
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

#
# TEMPLATES
#
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

import sys

from .base import *

#
# SENTRY
#
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

#
# LOGGING
#
# Production logging facility.
LOGGING['loggers'].update({
    'brouwers': {
        'handlers': ['project'],
        'level': 'WARNING',
        'propagate': True,
    },
    'django': {
        'handlers': ['django'],
        'level': 'WARNING',
        'propagate': True,
    },
})

try:
    from .secrets import *
except ImportError:
    sys.stderr.write("Create your secrets.py file with the secret settings.")

#
# STATICFILES
#
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

#
# SESSION
#
SESSION_COOKIE_DOMAIN = '.modelbrouwers.nl'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

#
# CACHE
#
CACHES['default']['KEY_PREFIX'] = 'production'

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

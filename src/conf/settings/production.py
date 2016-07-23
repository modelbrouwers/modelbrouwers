import sys

from .base import *

#
# SENTRY
#
INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

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
STATICFILES_STORAGE = 'systemjs.storage.SystemJSManifestStaticFilesStorage'

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
SECURE_HSTS_SECONDS = 0  # start really low

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

#
# THUMBNAILING
#
THUMBNAIL_DEBUG = False

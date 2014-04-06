from .base import *

try:
    from .secrets import *
except ImportError:
    sys.stderr.write("Create your secrets.py file with the secret settings.")


DEBUG = True
TEMPLATE_DEBUG = True

#
# Debug toolbar
#
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

#
# CACHE
#
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #     'LOCATION': '127.0.0.1:11211',
    # },
    # # 'database': {
    # #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    # #     'LOCATION': 'django_cache',
    # # },
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     'LOCATION': 'mb-django-cache',
    # }
}

#
# E-MAIL
#
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(PROJECT_ROOT, 'mails')

# SESSION
SESSION_COOKIE_NAME = 'mbsessionid'

# Local overrides
try:
    from .local_settings import *
except ImportError:
    pass
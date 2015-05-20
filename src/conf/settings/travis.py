from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

SECRET_KEY = 'uz1k)y8-)wxf5-(o43!(*+cnk6yd1ci1e4*@x$tad+0!dy)58+'

#
# CACHE
#
CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    # },
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION': 'django_cache',
    # },
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     'LOCATION': 'mb-django-cache',
    # }
}

# SESSION
SESSION_COOKIE_NAME = 'mbsessionid'

# Secrets
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    },
    'mysql': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    },
}

#
# HONEYPOT
#
HONEYPOT_URL = '/dummy.php'
HTTPBL_ACCESS_KEY = 'my-private-key'
# Value between 0 and 255, with 0 meaning no threat.
HTTPBL_MIN_THREAT_LEVEL = 10

#
# PHPBB
#
PHPBB_TABLE_PREFIX = 'phpbb3_'
PHPBB_URL = '/forum'
PHPBB_UID_COOKIE = 'phpbb3_u'

INSTALLED_APPS = INSTALLED_APPS + ('brouwers.forum_tools.tests.custom_fields',)

MEDIA_ROOT = os.path.join(ROOT_DIR, 'test_media')

SENDFILE_BACKEND = 'sendfile.backends.simple'

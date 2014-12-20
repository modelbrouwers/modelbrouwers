import sys
import os


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
ROOT_DIR = os.path.dirname(PROJECT_DIR)

if 'test' in sys.argv:
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

    MEDIA_ROOT = os.path.join(ROOT_DIR, 'test_media')


CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    # },
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    # 'database': {
    #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION': 'django_cache',
    # },
    # 'local_mem': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     'LOCATION': 'unique-snowflake'
    # }
}


# COMPRESS_ENABLED = False

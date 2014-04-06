import os
PROJECT_ROOT = os.path.dirname(os.path.realpath(os.path.join('..', '..', __file__)))

#
# Secret key
#
SECRET_KEY = 'tzt$*c-=)%9hi=#ce#lu!0+-6k3*6x@_%$r*j9-g85@v)_1^oa'

#
# Database settings
#
DATABASES = {
    'default': { # django postgres db
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'brouwers',
        'USER': 'brouwers',
        'PASSWORD': 'test',
    },
    'mysql': { # django mysql db
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'forum',
        'USER': 'brouwers',
        'PASSWORD': 'test',
    },
    'sqlite3': { #pure django development
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.normpath(os.path.join(PROJECT_ROOT, 'brouwers.db'))
    },
}

#
# When running in DEBUG=False
#
INTERNAL_IPS = ('127.0.0.1', '192.168.1.108', '192.168.1.138')

#
# Honeypot URL
#
HONEYPOT_URL = '/scratchy.php'
HTTPBL_ACCESS_KEY = 'yegymochlggr'
# Value between 0 and 255, with 0 meaning no threat.
HTTPBL_MIN_THREAT_LEVEL = 10

#
# MIBBIT CHAT
#
MIBBIT_SETTINGS = '61b92aae9db826980bf63939f88326f9'

#
# PHPBB3 integration
#
PHPBB_TABLE_PREFIX = 'phpbb_'
PHPBB_URL = '/phpBB3'
PHPBB_UID_COOKIE = 'phpbb3_10uny8_u'
from os.path import join, normpath, dirname, realpath
PROJECT_ROOT = dirname(dirname(dirname(realpath(__file__))))


SECRET_KEY = 'tzt$*c-=)%9hi=#ce#lu!0+-6k3*6x@_%$r*j9-g85@v)_1^oa'

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
        'NAME': normpath(join(PROJECT_ROOT, 'brouwers.db'))
    },
}

HTTPBL_ACCESS_KEY = 'yegymochlggr'

# MIBBIT CHAT
MIBBIT_SETTINGS = '61b92aae9db826980bf63939f88326f9'
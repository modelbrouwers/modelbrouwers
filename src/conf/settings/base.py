import os
from django.utils.translation import ugettext_lazy as _

# Automatically figure out the PROJECT DIR
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
ROOT_DIR = os.path.dirname(PROJECT_DIR)
BASE_DIR = ROOT_DIR

#
# GENERAL
#
SITE_ID = 1
DEBUG = False
DEVELOPMENT = False
TESTING = False

ADMINS = ()

TIME_ZONE = 'Europe/Amsterdam'
USE_TZ = True

USE_I18N = True

LANGUAGES = [
    ('en', _('English')),
    ('nl', _('Dutch')),
]

LOCALE_PATHS = [
    os.path.join(PROJECT_DIR, 'locale'),
]

USE_L10N = True
DATE_FORMAT = 'd-m-Y'

#
# LOGGING
#
LOGGING_DIR = os.path.join(ROOT_DIR, 'log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s %(module)s %(process)d %(thread)d  %(message)s'
        },
        'timestamped': {
            'format': '%(asctime)s %(levelname)s %(name)s  %(message)s'
        },
        'simple': {
            'format': '%(levelname)s  %(message)s'
        },
        'performance': {
            'format': '%(asctime)s %(process)d | %(thread)d | %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'timestamped'
        },
        'django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'django.log'),
            'formatter': 'verbose'
        },
        'project': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'brouwers.log'),
            'formatter': 'verbose'
        },
        'performance': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'performance.log'),
            'formatter': 'performance'
        },
    },
    'loggers': {
        'brouwers': {
            'handlers': ['project'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#
# MEDIA
#
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_ROOT = os.path.join(ROOT_DIR, 'media_sendfile')
SENDFILE_URL = '/protected'

#
# STATIC FILES
#
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
    # node_modules cannot be consistently installed in the 'correct place'.
    # symlinking resuls in too many levels of symlinks
    os.path.join(ROOT_DIR, 'node_modules'),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

#
# TEMPLATE
#
RAW_TEMPLATE_LOADERS = [
    'admin_tools.template_loaders.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False,  # conflicts with explicity specifying the loaders
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",

                "brouwers.general.context_processors.connection",
                "brouwers.general.context_processors.djsettings",
            ],
            'loaders': RAW_TEMPLATE_LOADERS
        },
    },
]

#
# MIDDLEWARE
#
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'sessionprofile.middleware.SessionProfileMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # after auth middleware, checks if user is authenticated
    'brouwers.banning.middleware.BanningMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

#
# URLS
#
ROOT_URLCONF = 'brouwers.urls'

#
# APPS
#
INSTALLED_APPS = [
    # Contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # admin tools. order is important
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',

    # Third party
    'compressor',
    'sessionprofile',
    'rest_framework',
    'django_extensions',
    'sniplates',
    'rosetta',
    'precise_bbcode',
    'sorl.thumbnail',
    'systemjs',

    # Modelbrouwers
    'brouwers.users',
    'brouwers.albums',
    'brouwers.awards',
    'brouwers.banning',
    'brouwers.builds',
    'brouwers.brouwersdag',
    'brouwers.forum_tools',
    'brouwers.general',
    'brouwers.groupbuilds',
    'brouwers.kitreviews',
    'brouwers.migration',
    'brouwers.online_users',
    'brouwers.secret_santa',
    'brouwers.shirts',
    'brouwers.utils',
]

#
# DATABASE
#
DATABASE_ROUTERS = [
    'brouwers.forum_tools.db_router.ForumToolsRouter'
]
# db config -> secrets.py

#
# CACHE
#
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
}

#
# SESSION
#
SESSION_COOKIE_NAME = 'mbsessionid'
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 60*60*24*7*365  # one year

#
# AUTH
#
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'brouwers.users.backends.EmailModelBackend',
]
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

SKIP_AUTH_USER_MODEL_MIGRATIONS = True

#
# MIBBIT
#
IRC_SERVER = 'irc.slacknet.org'
IRC_CHANNEL = '#modelbrouwers.nl'
IRC_DEFAULT_NICK = 'brouwer%3F%3F'


#
# TESTS
#
TEST_RUNNER = 'brouwers.utils.tests.runner.TestDiscoverRunner'

#################
# APP SPECIFICS #
#################

#
# Registration logging + bans
#
LOG_REGISTRATION_ATTEMPTS = True

#
# AWARDS
#
VOTE_END_MONTH = 1
VOTE_END_DAY = 15

#
# ALBUMS
#
VALID_IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png']
THUMB_DIMENSIONS = (200, 150, 'thumb_')

#
# FORUM_TOOLS
#
# in .secrets.py
TOPIC_DEAD_TIME = 1  # months

#
# COMPRESS
#
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

#
# ADMIN TOOLS
#
ADMIN_TOOLS_INDEX_DASHBOARD = 'brouwers.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'brouwers.dashboard.CustomAppIndexDashboard'

#
# WSGI conf
#
WSGI_APPLICATION = 'conf.wsgi.application'

#
# SORL THUMBNAIL
#
THUMBNAIL_DEBUG = True

#
# DRF
#
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'brouwers.api.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

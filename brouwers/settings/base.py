import os
import sys
# import django.conf.global_settings as DEFAULT_SETTINGS

# Automatically figure out the PROJECT DIR
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

#
# GENERAL
#
SITE_ID = 1
DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = ()

#
# TIMEZONE/LOCALISATION/TRANSLATION
#
gettext_noop = lambda s: s

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True
LANGUAGES = (
    ('en', gettext_noop('English')),
    ('nl', gettext_noop('Dutch')),
)
LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'locale'),)

USE_L10N = True
DATE_FORMAT = 'd-m-Y'

#
# MEDIA
#
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

#
# STATIC FILES
#
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'brouwers', 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

#
# TEMPLATE
#
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(PROJECT_ROOT, 'brouwers', 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",

    "albums.context_processors.user_is_album_admin",
    "general.context_processors.connection",
)

#
# MIDDLEWARE
#
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'sessionprofile.middleware.SessionProfileMiddleware',
    'albums.middleware.UploadifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # after auth middleware, checks if user is authenticated
    'banning.middleware.BanningMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

#
# URLS
#
ROOT_URLCONF = 'brouwers.urls'

#
# APPS
#
INSTALLED_APPS = (
    # Contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Third party
    'compressor',
    'sessionprofile',
    'south',
    'tastypie',
    'django_extensions',
    'django_nose',

    # Modelbrouwers
    'albums',
    'awards',
    'banning',
    'builds',
    'forum_tools',
    'general',
    'kitreviews',
    'migration',
    'online_users',
    'secret_santa',
    'shirts',
)

#
# DATABASE
#
DATABASE_ROUTERS = [
    'forum_tools.db_router.ForumToolsRouter'
]
#db config -> secrets.py

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
SESSION_COOKIE_AGE = 6048000

#
# AUTH
#
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_PROFILE_MODULE = 'general.UserProfile'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

#
# MIBBIT
#
IRC_SERVER = 'irc.slacknet.org'
IRC_CHANNEL = '#modelbrouwers.nl'
IRC_DEFAULT_NICK = 'brouwer%3F%3F'

#################
# APP SPECIFICS #
#################
#
# SOUTH
#
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

#
# Registration logging + bans
#
LOG_REGISTRATION_ATTEMPS = True

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

#
# COMPRESS
#
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

#
# NOSE
#
TEST_RUNNER = 'general.tests.utils.UnmanagedTablesTestRunner'

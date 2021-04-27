import os

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .utils import config

# Build paths inside the project, so further paths can be defined relative to
# the code root.
DJANGO_PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir)
)
BASE_DIR = os.path.abspath(
    os.path.join(DJANGO_PROJECT_DIR, os.path.pardir, os.path.pardir)
)

#
# Core Django settings
#
SITE_ID = config("SITE_ID", default=1)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# NEVER run with DEBUG=True in production-like environments
DEBUG = config("DEBUG", default=False)

# = domains we're running on
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", split=True)

IS_HTTPS = config("IS_HTTPS", default=not DEBUG)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGES = [
    ("en", _("English")),
    ("nl", _("Dutch")),
    ("de", _("German")),
]

# LANGUAGE_CODE = "nl"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = False

DATE_FORMAT = "d-m-Y"

#
# DATABASE and CACHING setup
#
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": config("DB_NAME", "brouwers"),
        "USER": config("DB_USER", "brouwers"),
        "PASSWORD": config("DB_PASSWORD", "brouwers"),
        "HOST": config("DB_HOST", "localhost"),
        "PORT": config("DB_PORT", 5432),
    },
    "mysql": {  # django mysql db
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("FORUM_DB_NAME", "brouwers"),
        "USER": config("FORUM_DB_USER", "brouwers"),
        "PASSWORD": config("FORUM_DB_PASSWORD", "brouwers"),
        "HOST": config("FORUM_DB_HOST", "localhost"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES', storage_engine=MYISAM",
        },
    },
}

DATABASE_ROUTERS = ["brouwers.forum_tools.db_router.ForumToolsRouter"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": config("CACHE_URL", "127.0.0.1:11211"),
        "KEY_PREFIX": config("CACHE_PREFIX", ""),
    },
}

#
# APPLICATIONS enabled for this project
#

INSTALLED_APPS = [
    # Contrib apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "modeltranslation",  # has to be imported before django.contrib.admin
    # admin tools. order is important
    "admin_tools",
    "admin_tools.theming",
    "admin_tools.menu",
    "admin_tools.dashboard",
    "django.contrib.admin",
    # Third party
    "compressor",
    "sessionprofile",
    "rest_framework",
    "django_filters",
    "rest_framework_filters",
    "loginas",
    "sniplates",
    "rosetta",
    "precise_bbcode",
    "sorl.thumbnail",
    "treebeard",
    "taggit",
    "ckeditor",
    "import_export",
    "solo",
    # Modelbrouwers
    "brouwers.users",
    "brouwers.albums",
    "brouwers.awards",
    "brouwers.banning",
    "brouwers.builds",
    "brouwers.brouwersdag",
    "brouwers.forum_tools",
    "brouwers.general",
    "brouwers.groupbuilds",
    "brouwers.kits",
    "brouwers.kitreviews",
    "brouwers.migration",
    "brouwers.online_users",
    "brouwers.utils",
    "brouwers.shop",
]

#
# MIDDLEWARE
#
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "sessionprofile.middleware.SessionProfileMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # after auth middleware, checks if user is authenticated
    "brouwers.banning.middleware.BanningMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
]

ROOT_URLCONF = "brouwers.urls"

TEMPLATE_LOADERS = [
    "admin_tools.template_loaders.Loader",
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": False,  # conflicts with explicity specifying the loaders
        "DIRS": [os.path.join(BASE_DIR, "src", "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
                "brouwers.general.context_processors.connection",
                "brouwers.general.context_processors.djsettings",
            ],
            "loaders": TEMPLATE_LOADERS,
        },
    },
]

WSGI_APPLICATION = "brouwers.wsgi.application"

LOCALE_PATHS = [
    os.path.join(DJANGO_PROJECT_DIR, "locale"),
]

#
# SERVING of static and media files
#
STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "src", "static"),
    # node_modules cannot be consistently installed in the 'correct place'.
    # symlinking results in too many levels of symlinks
    ("bootstrap", os.path.join(BASE_DIR, "node_modules", "bootstrap")),
    os.path.join(BASE_DIR, "node_modules", "fine-uploader"),
    ("font-awesome", os.path.join(BASE_DIR, "node_modules", "font-awesome")),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


SENDFILE_BACKEND = config("SENDFILE_BACKEND", "sendfile.backends.nginx")

SENDFILE_ROOT = os.path.join(BASE_DIR, "media_sendfile")

SENDFILE_URL = "/protected"

PRIVATE_MEDIA_URL = SENDFILE_URL

PRIVATE_MEDIA_ROOT = SENDFILE_ROOT

FILE_UPLOAD_PERMISSIONS = 0o644

#
# Sending EMAIL
#
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default=25)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False)
EMAIL_TIMEOUT = 10

SERVER_EMAIL = "beheer@modelbrouwers.nl"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", SERVER_EMAIL)

#
# LOGGING
#
LOG_STDOUT = config("LOG_STDOUT", default=False)

LOGGING_DIR = os.path.join(BASE_DIR, "log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(process)d %(thread)d  %(message)s"
        },
        "timestamped": {"format": "%(asctime)s %(levelname)s %(name)s  %(message)s"},
        "simple": {"format": "%(levelname)s  %(message)s"},
        "performance": {
            "format": "%(asctime)s %(process)d | %(thread)d | %(message)s",
        },
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "timestamped",
        },
        "django": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "django.log"),
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "project": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "brouwers.log"),
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "performance": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "performance.log"),
            "formatter": "performance",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
    },
    "loggers": {
        "brouwers": {
            "handlers": ["project"] if not LOG_STDOUT else ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["django", "mail_admins"]
            if not LOG_STDOUT
            else ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

#
# AUTH settings - user accounts, passwords, backends...
#
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "brouwers.users.backends.EmailModelBackend",
]

SESSION_COOKIE_NAME = "mbsessionid"

SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN", None)

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 365  # one year

SESSION_SAVE_EVERY_REQUEST = False

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SESSION_CACHE_ALIAS = "default"

LOGIN_URL = reverse_lazy("users:login")

LOGIN_REDIRECT_URL = reverse_lazy("index")

SKIP_AUTH_USER_MODEL_MIGRATIONS = True

#
# SECURITY settings
#
SESSION_COOKIE_SECURE = IS_HTTPS
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = IS_HTTPS

X_FRAME_OPTIONS = "DENY"

SECURE_SSL_REDIRECT = IS_HTTPS

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
VALID_IMG_EXTENSIONS = [".jpg", ".jpeg", ".png"]
THUMB_DIMENSIONS = (200, 150, "thumb_")

#
# FORUM_TOOLS
#
# in .secrets.py
TOPIC_DEAD_TIME = 1  # months

#
# COMPRESS
#
COMPRESS_ENABLED = not DEBUG

COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]

#
# ADMIN TOOLS
#
ADMIN_TOOLS_INDEX_DASHBOARD = "brouwers.dashboard.CustomIndexDashboard"
ADMIN_TOOLS_APP_INDEX_DASHBOARD = "brouwers.dashboard.CustomAppIndexDashboard"

#
# SORL THUMBNAIL
#
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_PRESERVE_FORMAT = True

#
# DRF
#
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "brouwers.api.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_filters.backends.RestFrameworkFilterBackend",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

#
# RAVEN/SENTRY
#
SENTRY_DSN = config("SENTRY_DSN", default="")

if SENTRY_DSN:
    RAVEN_CONFIG = {
        "dsn": SENTRY_DSN,
    }

    INSTALLED_APPS += [
        "raven.contrib.django.raven_compat",
    ]


#
# PHPBB
#
PHPBB_URL = "/phpBB3"
PHPBB_TABLE_PREFIX = "phpbb_"
PHPBB_POSTS_PER_PAGE = 10
PHPBB_UID_COOKIE = config("PHPBB_UID_COOKIE", "phpbb3_u")

# SECURITY
#
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

#
# CHAT
#
MIBBIT_SETTINGS = ""
IRC_SERVER = "irc.slacknet.org"
IRC_CHANNEL = "#modelbrouwers.nl"
IRC_DEFAULT_NICK = "brouwer%3F%3F"

#
# NEW SHOP
#
SHOP_ENABLED = False

#
# (UNIT) TESTING
#
TESTING = False

TEST_RUNNER = "brouwers.utils.tests.runner.TestDiscoverRunner"

import os

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import sentry_sdk
from sentry_sdk.integrations.logging import ignore_logger

from .utils import config, get_sentry_integrations

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
    ("nl", _("Dutch")),
    ("en", _("English")),
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
    "legacy_shop": {  # read data from the legacy shop database
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("LEGACY_SHOP_DB_NAME", "shop_brouwers"),
        "USER": config("LEGACY_SHOP_DB_USER", "brouwers"),
        "PASSWORD": config("LEGACY_SHOP_DB_PASSWORD", "brouwers"),
        "HOST": config("LEGACY_SHOP_DB_HOST", "localhost"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES', storage_engine=MYISAM",
        },
    },
}

# Change to BigAutoField on Django 4+
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DATABASE_ROUTERS = ["brouwers.db_router.Router"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
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
    "django_admin_index",
    "ordered_model",
    "django.contrib.admin",
    # Third party
    "sessionprofile",
    "rest_framework",
    "django_bleach",
    "django_filters",
    "rest_framework_filters",
    "loginas",
    "sniplates",
    "rosetta",
    "sorl.thumbnail",
    "treebeard",
    "taggit",
    "ckeditor",
    "import_export",
    "solo",
    "corsheaders",
    "django_recaptcha",
    # Modelbrouwers
    "brouwers.users",
    "brouwers.albums",
    "brouwers.anniversaries",
    "brouwers.awards",
    "brouwers.banning",
    "brouwers.builds",
    "brouwers.brouwersdag",
    "brouwers.contact",
    "brouwers.emails",
    "brouwers.forum_tools",
    "brouwers.general",
    "brouwers.groupbuilds",
    "brouwers.kits",
    "brouwers.kitreviews",
    "brouwers.online_users",
    "brouwers.utils",
    "brouwers.legacy_shop",
    "brouwers.shop",
]

#
# MIDDLEWARE
#
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
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


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
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
                "brouwers.shop.context_processors.cart",
            ],
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
]

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


SENDFILE_BACKEND = config("SENDFILE_BACKEND", "django_sendfile.backends.nginx")

SENDFILE_ROOT = os.path.join(BASE_DIR, "media_sendfile")

SENDFILE_URL = "/protected"

PRIVATE_MEDIA_URL = SENDFILE_URL

PRIVATE_MEDIA_ROOT = SENDFILE_ROOT

FILE_UPLOAD_PERMISSIONS = 0o644

FIXTURE_DIRS = [
    os.path.join("DJANGO_PROJECT_DIR", "fixtures"),
]

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

# Custom settings for email flows
EMAIL_CONTACT_NOTIFICATION = config("EMAIL_CONTACT_NOTIFICATION", default=SERVER_EMAIL)

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
            "handlers": (
                ["django", "mail_admins"]
                if not LOG_STDOUT
                else ["console", "mail_admins"]
            ),
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

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

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

SILENCED_SYSTEM_CHECKS = ["debug_toolbar.W006"]

#
# Custom settings
#
ENVIRONMENT = config("ENVIRONMENT", "")

if "GIT_SHA" in os.environ:
    GIT_SHA = config("GIT_SHA", "")
# in docker (build) context, there is no .git directory
elif os.path.exists(os.path.join(BASE_DIR, ".git")):
    try:
        import git
    except ImportError:
        GIT_SHA = None
    else:
        repo = git.Repo(search_parent_directories=True)
        try:
            GIT_SHA = repo.head.object.hexsha
        except (
            ValueError
        ):  # on startproject initial runs before any git commits have been made
            GIT_SHA = repo.active_branch.name
else:
    GIT_SHA = None

RELEASE = config("RELEASE", GIT_SHA)

GEOIP_DATABASE_PATH = config(
    "GEOIP_DATABASE_PATH", default="/tmp/geoip/GeoLite2-Country.mmdb"
)

#################
# APP SPECIFICS #
#################

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
# SORL THUMBNAIL
#
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_PRESERVE_FORMAT = True

#
# DJANGO-ADMIN-INDEX
#
ADMIN_INDEX_SHOW_REMAINING_APPS = True

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
# SENTRY
#
SENTRY_DSN = config("SENTRY_DSN", default="")

if SENTRY_DSN:
    SENTRY_CONFIG = {
        "dsn": SENTRY_DSN,
        "release": RELEASE,
        "environment": ENVIRONMENT,
    }

    sentry_sdk.init(
        **SENTRY_CONFIG, integrations=get_sentry_integrations(), send_default_pii=True
    )
    ignore_logger("sorl.thumbnail")
    ignore_logger("sorl.thumbnail.base")

#
# CORSHEADERS
#
CORS_ORIGIN_ALLOW_ALL = config("CORS_ENABLED", default=False)
CORS_ALLOW_CREDENTIALS = config("CORS_ENABLED", default=False)

#
# DJANGO-BLEACH
#
BLEACH_ALLOWED_TAGS = {
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "em",
    "i",
    "li",
    "ol",
    "strong",
    "ul",
    "s",
    "p",
    "div",
    "br",
    "img",
    "hr",
}
BLEACH_ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel"],
    "abbr": ["title"],
    "acronym": ["title"],
    "img": ["src", "alt", "height", "width"],
}
BLEACH_STRIP_TAGS = True

#
# DJANGO-RECAPTCHA
#
RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY", default="")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY", default="")

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
# DJANGO-MODELTRANSLATION
#
MODELTRANSLATION_FALLBACK_LANGUAGES = ("nl", "en")

#
# CHAT
#
MIBBIT_SETTINGS = ""
IRC_SERVER = "irc.slacknet.org"
IRC_CHANNEL = "#modelbrouwers.nl"
IRC_DEFAULT_NICK = "brouwer%3F%3F"

#
# SHOP
#

# TODO: move to singleton config
SHOP_BRAND_NAME = config("SHOP_BRAND_NAME", "Modelbrouwers")

#
# (UNIT) TESTING
#
TESTING = False

TEST_RUNNER = "brouwers.utils.tests.runner.TestDiscoverRunner"

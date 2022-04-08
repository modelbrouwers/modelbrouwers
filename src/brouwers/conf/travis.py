import os

os.environ.setdefault("SECRET_KEY", "travis-key")
os.environ.setdefault("IS_HTTPS", "no")

os.environ.setdefault("DB_NAME", "brouwers")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "")

from .base import *  # noqa isort:skip

# Secrets
DATABASES["mysql"] = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}

# Regular settings
SESSION_ENGINE = "django.contrib.sessions.backends.db"

#
# PHPBB
#
PHPBB_TABLE_PREFIX = "phpbb3_"
PHPBB_URL = "/forum"
PHPBB_UID_COOKIE = "phpbb3_u"

INSTALLED_APPS = INSTALLED_APPS + ["brouwers.forum_tools.tests.custom_fields"]

MEDIA_ROOT = os.path.join(BASE_DIR, "test_media")

SENDFILE_BACKEND = "sendfile.backends.nginx"

SHOP_ENABLED = True

import os
import sys
import warnings

os.environ.setdefault("DEBUG", "yes")
os.environ.setdefault("ALLOWED_HOSTS", "*")
os.environ.setdefault("SECRET_KEY", "dev-key")
os.environ.setdefault("IS_HTTPS", "no")
os.environ.setdefault("SENDFILE_BACKEND", "sendfile.backends.development")
os.environ.setdefault("CORS_ENABLED", "yes")

from .base import *  # noqa isort:skip

SESSION_ENGINE = "django.contrib.sessions.backends.db"

#
# Debug toolbar
#
INSTALLED_APPS += [
    "django_extensions",
    "debug_toolbar",
]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ("127.0.0.1",)
DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": "",
}

# Custom settings
SHOP_ENABLED = True

#
# E-MAIL
#
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# SESSION
SESSION_COOKIE_NAME = "mbsessionid"

# THOU SHALT NOT USE NAIVE DATETIMES
warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)

# Local overrides
try:
    from .local import *  # noqa
except ImportError:
    pass


if "test" in sys.argv:
    INSTALLED_APPS += ["brouwers.forum_tools.tests.custom_fields"]
    SENDFILE_BACKEND = "sendfile.backends.nginx"

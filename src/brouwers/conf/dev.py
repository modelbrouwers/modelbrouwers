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
INSTALLED_APPS = INSTALLED_APPS + [
    "django_extensions",
    "debug_toolbar",
]

DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": "",
}

INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware",] + MIDDLEWARE

SHOP_ENABLED = True

#
# E-MAIL
#
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "mails")

# SESSION
SESSION_COOKIE_NAME = "mbsessionid"

# Local overrides
try:
    from .local import *  # noqa
except ImportError:
    pass


if "test" in sys.argv:
    INSTALLED_APPS += ["brouwers.forum_tools.tests.custom_fields"]
    SENDFILE_BACKEND = "sendfile.backends.nginx"


warnings.filterwarnings(
    "error", module=r"django\.db\.models\.query",
)

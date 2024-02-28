"""
Production environment settings module.
Tweaks the base settings so that caching mechanisms are used where possible,
and HTTPS is leveraged where possible to further secure things.
"""
import os

os.environ.setdefault("SESSION_COOKIE_DOMAIN", ".modelbrouwers.nl")
os.environ.setdefault("ALLOWED_HOSTS", ".modelbrouwers.nl")
os.environ.setdefault("CACHE_PREFIX", "production")

from .base import *  # noqa isort:skip


# The file storage engine to use when collecting static files with the
# collectstatic management command.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

#
# LOGGING
#
handlers = ["console"] if LOG_STDOUT else ["django"]

LOGGING["loggers"].update(
    {
        "django": {"handlers": handlers, "level": "INFO", "propagate": True},
        "django.security.DisallowedHost": {
            "handlers": handlers,
            "level": "CRITICAL",
            "propagate": False,
        },
    }
)

# Only set this when we're behind a reverse proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True  # Sets X-Content-Type-Options: nosniff
SECURE_BROWSER_XSS_FILTER = True  # Sets X-XSS-Protection: 1; mode=block

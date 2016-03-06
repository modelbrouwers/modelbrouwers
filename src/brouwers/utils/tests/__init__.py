import sys
from importlib import import_module

from django.conf import settings
from django.core.urlresolvers import clear_url_caches


def reload_urlconf():
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
        clear_url_caches()
    return import_module(settings.ROOT_URLCONF)

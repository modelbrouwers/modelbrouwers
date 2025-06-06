import sys
from importlib import import_module, reload

from django.conf import settings
from django.urls import clear_url_caches


def reload_urlconf():
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
        clear_url_caches()
    return import_module(settings.ROOT_URLCONF)


def is_testing():
    test_app = "brouwers.forum_tools.tests.custom_fields"
    return test_app in settings.INSTALLED_APPS

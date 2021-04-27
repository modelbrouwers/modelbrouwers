from django.apps import AppConfig
from django.test import SimpleTestCase, TestCase, TransactionTestCase
from django.utils.translation import ugettext_lazy as _


class GeneralConfig(AppConfig):
    name = "brouwers.general"
    verbose_name = _("General")

    def ready(self):
        from . import signals  # noqa

        monkeypatch_multi_db()


def monkeypatch_multi_db():
    SimpleTestCase.databases = "__all__"
    TransactionTestCase.databases = "__all__"
    TestCase.databases = "__all__"

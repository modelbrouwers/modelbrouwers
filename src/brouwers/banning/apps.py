from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BanningConfig(AppConfig):
    name = "brouwers.banning"
    verbose_name = _("Banning")

    def ready(self):
        from . import signals  # noqa

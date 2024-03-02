from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GroupbuildsConfig(AppConfig):
    name = "brouwers.groupbuilds"
    verbose_name = _("Groupbuilds")

    def ready(self):
        from . import signals

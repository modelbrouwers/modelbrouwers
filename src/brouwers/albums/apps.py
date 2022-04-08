from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AlbumsConfig(AppConfig):
    name = "brouwers.albums"
    verbose_name = _("Albums")

    def ready(self):
        from . import signals

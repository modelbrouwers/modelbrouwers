from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    name = 'brouwers.users'
    verbose_name = _('Users')

    def ready(self):
        from . import signals

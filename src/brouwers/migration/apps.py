from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MigrationConfig(AppConfig):
    name = 'brouwers.migration'
    verbose_name = _('Migrations')

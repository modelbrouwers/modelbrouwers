from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KitsConfig(AppConfig):
    name = 'brouwers.kits'
    verbose_name = _('kits')

    def ready(self):
        # register the custom extractor
        from sniplates.templatetags.sniplates import EXTRACTOR
        from .extractors import ModelKitExtractor
        EXTRACTOR['MultipleKitChoiceField'] = ModelKitExtractor

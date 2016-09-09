from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KitsConfig(AppConfig):
    name = 'brouwers.kits'
    verbose_name = _('kits')

    def ready(self):
        # register the custom extractors
        from sniplates.templatetags.sniplates import EXTRACTOR
        from .extractors import ModelKitExtractor, MultiModelKitExtractor
        EXTRACTOR['KitChoiceField'] = ModelKitExtractor
        EXTRACTOR['MultipleKitChoiceField'] = MultiModelKitExtractor

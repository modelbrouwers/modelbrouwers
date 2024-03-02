from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import CountryChoices

# TODO: refactor to django-countries


class CountryField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("verbose_name", _("country"))
        kwargs["choices"] = CountryChoices.choices
        kwargs["max_length"] = 1
        super().__init__(*args, **kwargs)

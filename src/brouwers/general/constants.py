from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO: refactor to django-countries
# See also the shop.tests.factories.AddressFactory
class CountryChoices(models.TextChoices):
    nl = "N", _("The Netherlands")
    be = "B", _("Belgium")
    de = "D", _("Germany")

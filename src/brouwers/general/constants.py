from django.utils.translation import gettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


# TODO: refactor to django-countries
class CountryChoices(DjangoChoices):
    nl = ChoiceItem("N", _("The Netherlands"))
    be = ChoiceItem("B", _("Belgium"))
    de = ChoiceItem("D", _("Germany"))
    fr = ChoiceItem("F", _("France"))

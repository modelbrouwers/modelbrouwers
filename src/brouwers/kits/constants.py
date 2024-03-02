from django.db import models
from django.utils.translation import gettext_lazy as _


class KitDifficulties(models.IntegerChoices):
    very_easy = 10, _("very easy")
    easy = 20, _("easy")
    medium = 30, _("medium")
    hard = 40, _("hard")
    very_hard = 50, _("very hard")

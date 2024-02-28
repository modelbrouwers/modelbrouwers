from django.db import models
from django.utils.translation import gettext_lazy as _


class VoteTypes(models.TextChoices):
    positive = "+", "+"
    negative = "-", "-"

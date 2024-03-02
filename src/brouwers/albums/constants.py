from django.db import models
from django.utils.translation import gettext_lazy as _, pgettext_lazy


class WritePermissions(models.TextChoices):
    owner = "u", pgettext_lazy("write permissions for owner", "owner")
    everyone = "o", _("everyone")  # auth required

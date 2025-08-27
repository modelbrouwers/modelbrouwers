from django.db import models


class VoteTypes(models.TextChoices):
    positive = "+", "+"
    negative = "-", "-"

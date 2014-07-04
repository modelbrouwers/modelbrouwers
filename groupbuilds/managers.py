from datetime import timedelta

from django.db import models
from django.utils import timezone


class PublicGroupBuildsManager(models.Manager):
    """ Publicly visible photos """

    def get_query_set(self):
        from .models import GroupbuildStatuses # avoid circular imports
        date_limit = timezone.now() - timedelta(days=14)
        base_qs = super(PublicGroupBuildsManager, self).get_query_set()
        return base_qs.filter(
            status__in=GroupbuildStatuses.public_statuses
        ).filter(
            models.Q(end__gte=date_limit) | models.Q(end=None)
        )

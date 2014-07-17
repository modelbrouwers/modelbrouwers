from datetime import timedelta

from django.db.models import Q, Manager
from django.utils import timezone


class PublicGroupBuildsManager(Manager):
    """ Publicly visible photos """

    def get_query_set(self):
        base_qs = super(PublicGroupBuildsManager, self).get_query_set()
        from .models import GroupbuildStatuses # avoid circular imports
        date_limit = timezone.now() - timedelta(days=14)
        q_end_date = Q(Q(end__gte=date_limit) & Q(status__in=GroupbuildStatuses.date_bound_statuses))
        q_end_date |= Q(status__in=GroupbuildStatuses.non_date_bound_statuses)
        return base_qs.filter(status__in=GroupbuildStatuses.public_statuses).filter(q_end_date)

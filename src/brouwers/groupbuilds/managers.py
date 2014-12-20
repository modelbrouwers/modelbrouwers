from datetime import timedelta

from django.db.models import Q, Manager
from django.utils import timezone


class PublicGroupBuildsManager(Manager):
    """ Publicly visible photos """

    def get_base_query_set(self):
        return super(PublicGroupBuildsManager, self).get_query_set()

    def get_query_set(self):
        from .models import GroupbuildStatuses # avoid circular imports
        base_qs = self.get_base_query_set()
        date_limit = timezone.now() - timedelta(days=14)
        q_end_date = Q(Q(end__gte=date_limit) | Q(end=None)) & Q(status__in=GroupbuildStatuses.date_bound_statuses)
        q_end_date |= Q(status__in=GroupbuildStatuses.non_date_bound_statuses)
        return base_qs.filter(status__in=GroupbuildStatuses.public_statuses).filter(q_end_date)

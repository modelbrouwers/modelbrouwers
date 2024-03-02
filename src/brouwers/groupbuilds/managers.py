from datetime import timedelta

from django.db.models import Manager, Q
from django.utils import timezone

from .constants import DATE_BOUND_STATUSES, NON_DATE_BOUND_STATUSES, PUBLIC_STATUSES
from .query import GroupbuildQuerySet


class PublicGroupBuildsManager(Manager.from_queryset(GroupbuildQuerySet)):
    """Publicly visible groupbuilds"""

    def get_base_queryset(self):
        return super().get_queryset()

    def get_queryset(self):
        base_qs = self.get_base_queryset()
        date_limit = timezone.now() - timedelta(days=14)
        q_end_date = Q(Q(end__gte=date_limit) | Q(end=None)) & Q(
            status__in=DATE_BOUND_STATUSES
        )
        q_end_date |= Q(status__in=NON_DATE_BOUND_STATUSES)
        return base_qs.filter(status__in=PUBLIC_STATUSES).filter(q_end_date)

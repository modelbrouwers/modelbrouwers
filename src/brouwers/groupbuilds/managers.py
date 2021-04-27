from datetime import timedelta

from django.db.models import Manager, Q
from django.utils import timezone

from .query import GroupbuildQuerySet


class PublicGroupBuildsManager(Manager.from_queryset(GroupbuildQuerySet)):
    """Publicly visible groupbuilds"""

    def get_base_queryset(self):
        return super().get_queryset()

    def get_queryset(self):
        from .models import GroupbuildStatuses  # avoid circular imports

        base_qs = self.get_base_queryset()
        date_limit = timezone.now() - timedelta(days=14)
        q_end_date = Q(Q(end__gte=date_limit) | Q(end=None)) & Q(
            status__in=GroupbuildStatuses.date_bound_statuses
        )
        q_end_date |= Q(status__in=GroupbuildStatuses.non_date_bound_statuses)
        return base_qs.filter(status__in=GroupbuildStatuses.public_statuses).filter(
            q_end_date
        )

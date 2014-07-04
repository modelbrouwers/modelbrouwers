from django.views.generic import ListView
from django.utils import timezone

from .models import GroupBuild, GroupbuildStatuses as GBStatuses


class GroupBuildListView(ListView):
    model = GroupBuild

    def get_queryset(self):
        return GroupBuild.public.all()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'statuses': GBStatuses.choices
        })
        return super(GroupBuildListView, self).get_context_data(**kwargs)

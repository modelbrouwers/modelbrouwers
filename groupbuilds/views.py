from django.views.generic import ListView
from django.utils import timezone

from .models import GroupBuild


class GroupBuildListView(ListView):
    model = GroupBuild

    def get_queryset(self):
        return GroupBuild.public.all()

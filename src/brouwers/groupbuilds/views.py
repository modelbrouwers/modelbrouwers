from django.views.generic import DetailView, ListView

from .constants import GroupbuildStatuses
from .models import GroupBuild


class GroupBuildListView(ListView):
    """
    Archived list of group builds.
    """

    queryset = GroupBuild.objects.filter(
        status__in=[
            GroupbuildStatuses.accepted,
            GroupbuildStatuses.extended,
        ]
    ).order_by("-start", "-end")
    context_object_name = "group_builds"


class GroupBuildDetailView(DetailView):
    queryset = GroupBuild.objects.filter(
        status__in=[
            GroupbuildStatuses.accepted,
            GroupbuildStatuses.extended,
        ]
    )
    context_object_name = "gb"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        participants = self.object.participant_set.select_related("user").order_by("id")
        context["participants"] = participants

        if user.is_authenticated:
            context["own_models"] = [p for p in participants if p.user_id == user.id]

        return context

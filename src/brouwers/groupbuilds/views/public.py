from django.views.generic import DetailView

from ..forms import ParticipantForm
from .mixins import GroupBuildDetailMixin


class GroupBuildDetailView(GroupBuildDetailMixin, DetailView):
    context_object_name = "gb"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.object.is_open:
            ctx["participate_form"] = ParticipantForm()
        return ctx

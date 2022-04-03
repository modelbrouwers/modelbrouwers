""" Groupbuild participant views """
from datetime import date

from django.contrib import messages
from django.db.models import Count, Q
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.detail import (
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin
)

from brouwers.utils.views import LoginRequiredMixin

from ..forms import ParticipantForm
from ..models import GroupBuild, Participant
from .mixins import GroupBuildDetailMixin


class GroupBuildParticipateView(
    LoginRequiredMixin,
    GroupBuildDetailMixin,
    CreateView,
    SingleObjectTemplateResponseMixin,
    SingleObjectMixin,
):
    """GroupBuildDetailMixin makes this almost a GroupBuild DetailView."""

    model = Participant
    form_class = ParticipantForm
    context_object_name = "gb"
    template_name = "groupbuilds/groupbuild_detail.html"

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        form.instance.groupbuild = (
            self.get_object()
        )  # TODO: limit queryset to open groupbuilds
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _("You're now listed as participant!"))
        return response

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["participate_form"] = context["form"]
        return context


class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm

    def get_queryset(self):
        filters = {
            "groupbuild__slug": self.kwargs.get("slug"),
            "user": self.request.user,
        }
        today = date.today()
        q_end = Q(groupbuild__end__gt=today) | Q(groupbuild__end=None)
        return Participant.objects.select_related("groupbuild").filter(q_end, **filters)

    def get_context_data(self, **kwargs):
        kwargs["gb"] = self.object.groupbuild
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.object.groupbuild.get_absolute_url()


class MyGroupbuildsListView(LoginRequiredMixin, ListView):
    model = GroupBuild
    template_name = "groupbuilds/dashboard.html"

    def get_queryset(self):
        user = self.request.user
        self.admin_gbs = user.admin_groupbuilds.annotate(
            n_participants=Count("participants")
        ).order_by("id")
        self.participant_gbs = user.groupbuilds.annotate(
            n_participants=Count("participants")
        ).order_by("id")
        return (self.admin_gbs | self.participant_gbs).distinct().order_by("start")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["admin_gbs"] = self.admin_gbs
        context["participant_gbs"] = self.participant_gbs
        return context

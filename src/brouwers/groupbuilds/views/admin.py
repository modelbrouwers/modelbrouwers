""" Groupbuild administrator views """
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView

from brouwers.utils.views import LoginRequiredMixin

from ..forms import GroupBuildForm, SubmitForm
from ..models import GroupBuild, GroupbuildStatuses as GBStatuses
from .mixins import GroupBuildDetailMixin


class GroupBuildCreateView(LoginRequiredMixin, CreateView):
    model = GroupBuild
    template_name = "groupbuilds/create.html"
    form_class = GroupBuildForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_initial(self):
        initial = super().get_initial()
        initial["admins"] = self.request.user
        return initial


class GroupBuildUpdateView(LoginRequiredMixin, UpdateView):
    model = GroupBuild
    template_name = "groupbuilds/edit.html"
    form_class = GroupBuildForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_queryset(self):
        if self.request.user.is_superuser:
            return GroupBuild.objects.all()
        return self.request.user.admin_groupbuilds.exclude(status=GBStatuses.submitted)


class GroupBuildSubmitView(LoginRequiredMixin, GroupBuildDetailMixin, UpdateView):
    """View to submit the group build to the staff"""

    form_class = SubmitForm
    context_object_name = "gb"
    template_name = "groupbuilds/groupbuild_submit.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return self.request.user.admin_groupbuilds.with_admin_count()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            _("Your group build has been submitted to the moderator team."),
        )
        return response

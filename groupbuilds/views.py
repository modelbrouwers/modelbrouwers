from datetime import timedelta
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone

from utils.views import LoginRequiredMixin

from .models import GroupBuild, GroupbuildStatuses as GBStatuses
from .forms import GroupBuildForm


class GroupBuildListView(ListView):
    model = GroupBuild

    def get_queryset(self):
        return GroupBuild.public.all()

    def get_context_data(self, **kwargs):
        now = timezone.now()

        new_concepts = self.object_list.filter(status=GBStatuses.concept).order_by('?')[:5]
        starting_soon = self.object_list.filter(
            status=GBStatuses.accepted,
            start__gte=now + timedelta(days=3),
            start__lte=now + timedelta(weeks=6)
        ).order_by('start')

        calender_builds = self.object_list.filter(
            status__in=GBStatuses.date_bound_statuses
        )

        dates = [now.date()]

        kwargs.update({
            'statuses': GBStatuses.choices,
            'new_concepts': new_concepts,
            'starting_soon': starting_soon,
            'calender_builds': calender_builds,
            'dates': dates,
        })
        return super(GroupBuildListView, self).get_context_data(**kwargs)


class GroupBuildCreateView(LoginRequiredMixin, CreateView):
    model = GroupBuild
    template_name = 'groupbuilds/create.html'
    form_class = GroupBuildForm

    def get_form_kwargs(self):
        kwargs = super(GroupBuildCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_initial(self):
        initial = super(GroupBuildCreateView, self).get_initial()
        initial['admins'] = self.request.user
        return initial


class GroupBuildDetailView(DetailView):
    model = GroupBuild
    queryset = GroupBuild.public.all()
    context_object_name = 'gb'

    def get_queryset(self): # TODO: unit test
        user = self.request.user
        if user.is_authenticated(): # TODO: add staff permissions
            return (user.admin_groupbuilds.all() | self.queryset).distinct()
        return super(GroupBuildDetailView, self).get_queryset()

    def get_context_data(self, **kwargs):
        ctx = super(GroupBuildDetailView, self).get_context_data(**kwargs)
        ctx['participants'] = self.object.participant_set.all().order_by('id')
        return ctx


class GroupBuildUpdateView(LoginRequiredMixin, UpdateView):
    model = GroupBuild
    template_name = 'groupbuilds/edit.html'
    form_class = GroupBuildForm

    def get_form_kwargs(self):
        kwargs = super(GroupBuildUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_queryset(self):
        if self.request.user.is_superuser:
            return GroupBuild.objects.all()
        return self.request.user.admin_groupbuilds.all()

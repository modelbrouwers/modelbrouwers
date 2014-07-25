from django.views.generic import ListView, CreateView, DetailView, UpdateView

from utils.views import LoginRequiredMixin

from .models import GroupBuild, GroupbuildStatuses as GBStatuses
from .forms import GroupBuildForm


class GroupBuildListView(ListView):
    model = GroupBuild

    def get_queryset(self):
        return GroupBuild.public.all()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'statuses': GBStatuses.choices
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

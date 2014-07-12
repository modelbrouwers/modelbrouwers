from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView

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

    def get_success_url(self):
        return reverse('groupbuilds:edit', kwargs={'slug': self.object.slug})

    def get_initial(self):
        initial = super(GroupBuildCreateView, self).get_initial()
        initial['admins'] = self.request.user
        return initial

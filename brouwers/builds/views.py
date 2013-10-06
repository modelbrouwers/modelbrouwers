from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView


from general.models import UserProfile
from awards.models import Project


from .forms import BrouwerSearchForm
from .models import Build
from .forms import BuildForm


""" Views responsible for displaying data """


class BuildDetailView(DetailView):
    context_object_name = 'build'
    template_name = 'builds/build.html'
    model = Build


class BuildRedirectView(SingleObjectMixin, RedirectView):
    """ Get the build by pk, redirect to the slug url """
    permanent = True
    model = Build
    pk_url_kwarg = 'build_id'

    def get_redirect_url(self, **kwargs):
        self.build = self.get_object()
        return self.build.get_absolute_url()


class ProfileRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs):
        profile_id = self.kwargs.get('profile_id', None)
        profile = get_object_or_404(UserProfile, pk=profile_id)
        return reverse('builds:user_build_list', kwargs={'user_id': profile.user.id})


class UserBuildListView(ListView):
    context_object_name = 'builds'
    template_name = 'builds/profile_builds.html'
    paginate_by = 50

    def __init__(self, *args, **kwargs):
        super(UserBuildListView, self).__init__(*args, **kwargs)
        self.user_id = None

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        self.user = get_object_or_404(User, pk=user_id)
        return Build.objects.filter(user_id=user_id)

    def get_context_data(self, **kwargs):
        context = super(UserBuildListView, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context


# TODO: replace with ListView
def builders_overview(request):
    if request.method == "POST":
        form = BrouwerSearchForm(request.POST)
        if form.is_valid():
            brouwer = form.cleaned_data['nickname']
            profiles = UserProfile.objects.filter(forum_nickname__icontains = brouwer).order_by('forum_nickname')
            form = BrouwerSearchForm()
            return render(request, 'builds/profile_list.html', {'profiles': profiles, 'form': form})
    else:
        form = BrouwerSearchForm()
    builds = Build.objects.all().order_by('-pk')[:15]
    return render(request, 'builds/base.html', {'form': form, 'builds': builds})



""" Views responsible for editing data """


class BuildCreate(CreateView):
    form_class = BuildForm
    template_name = 'builds/add.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.profile = self.request.user.get_profile()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(BuildCreate, self).get_context_data(**kwargs)
        # show last 20 builds
        context['builds'] = Build.objects.all().order_by('-pk')[:20]
        return context


class BuildUpdate(BuildCreate, UpdateView):
    template_name = 'builds/edit.html'

    def get_queryset(self):
        if self.request.user.has_perms('builds.edit_build'):
            return Build.objects.all()
        return Build.objects.filter(user_id=self.request.user.id)


    def get_form_kwargs(self):
        kwargs = super(BuildUpdate, self).get_form_kwargs()
        kwargs.update({'is_edit': True})
        return kwargs


@login_required
def edit(request, id):
    build = get_object_or_404(Build, pk=id)
    if request.method == "POST":
        form = BuildForm(request.POST, instance=build)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(build.get_absolute_url())
    else:
        if request.user.groups.filter(name__iexact="moderators"):
            form = BuildForm(instance=build)
        else:
            if (build.profile != request.user.get_profile()):
                return HttpResponseRedirect(reverse(builders_overview))
        form = BuildForm(instance=build)
    return render(request, 'builds/edit.html', {'form': form})

from django.views.generic.list_detail import object_detail

#TODO: fix backlooping
def custom_object_detail(request, queryset, object_id=None, template_name=None, template_object_name='object'):
    object_id = int(object_id)
    queryset_new = queryset.filter(pk=object_id)
    while (not queryset_new and object_id < queryset.order_by('-pk')[0].pk):
        object_id += 1
        queryset_new = queryset.filter(pk=object_id)
    return object_detail(request, queryset_new, object_id, template_name=template_name, template_object_name=template_object_name)
    
    
    
    

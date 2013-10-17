from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView, RedirectView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView


from general.models import UserProfile
from awards.models import Project


from .forms import SearchForm, BuildForm, BuildFormForum, EditBuildForm
from .models import Build


import json


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
        context['builds_user'] = self.user
        return context


class SearchMixin(object):
    def get_search_queryset(self, form=None, key='term'):
        # TODO: look into Haystack/Whoosh for relevance ordered results
        if form:
            search_term = form.cleaned_data['search_term']
        else:
            search_term = self.request.GET.get(key, '')
        
        qs = Build.objects.all()
        for term in search_term.split():
            qs = qs.filter(slug__icontains=term)
        return qs.select_related('user', 'profile', 'brand')


class AjaxSearchView(SearchMixin, View):
    """ 
    Ajax search form suitable for jQuery-ui's 
    autocomplete.
    """

    field_for_value = 'id'
    field_for_label = 'title'

    def get(self, request, *args, **kwargs):
        objects = self.get_search_queryset(key='term')

        # serialize data
        data = self.serialize(objects)
        return HttpResponse(json.dumps(data), mimetype="application/json")

    def get_label(self, obj):
        """ Returns the visible label """
        return getattr(obj, self.field_for_label)

    def get_additional_data(self, obj):
        """ 
        Return a dictionary with keys the json key and value the
        object value
        """
        return {}
    
    def serialize(self, objects):
        data = []
        for obj in objects:
            d = {
                'value': getattr(obj, self.field_for_value, None),
                'label': self.get_label(obj),
            }
            d.update(self.get_additional_data(obj))
            data.append(d)
        return data


class BuildAjaxSearchView(AjaxSearchView):
    field_for_value = 'title'

    def get_label(self, obj):
        label = u"%s \u2022 %s" % (obj.profile.forum_nickname, obj.title)
        return mark_safe(label)

    def get_additional_data(self, obj):
        return {'url': obj.get_absolute_url()}


""" Views responsible for editing data """

class BuildCreate(CreateView, SearchMixin):
    """
    Both the index page and create page.
    """

    form_class = BuildForm
    template_name = 'builds/add.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_form_kwargs(self):
        """
        When Javascript is turned off, the user has a direct link with initial
        data. The form can be prefilled with this data.
        """
        kwargs = super(BuildCreate, self).get_form_kwargs()
        if self.request.method == 'GET' and 'prefill' in self.request.GET:
            form = BuildFormForum(self.request, self.request.GET)
            if form.is_valid():
                kwargs['instance'] = form.get_build()
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.profile = self.request.user.get_profile()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs['builds'] = Build.objects.all().select_related(
                            'user', 'profile', 'brand'
                            ).order_by('-pk')[:20] # TODO: paginate
        
        args = []
        if 'search-button' in self.request.GET:
            args.append(self.request.GET)
            form = SearchForm(*args)
            if form.is_valid():
                builds = self.get_search_queryset(form)
                kwargs.update({'builds': builds})

        
        kwargs['searchform'] = SearchForm(*args)
        return super(BuildCreate, self).get_context_data(**kwargs)


class BuildUpdate(UpdateView):
    form_class = EditBuildForm
    template_name = 'builds/edit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_queryset(self):
        if self.request.user.has_perms('builds.edit_build'):
            return Build.objects.all()
        return Build.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        kwargs['builds'] = Build.objects.filter(
                                user = self.request.user
                            ).select_related(
                                'user', 'profile', 'brand'
                            ).order_by('-pk')[:20]
        
        kwargs['searchform'] = SearchForm()
        return super(BuildUpdate, self).get_context_data(**kwargs)

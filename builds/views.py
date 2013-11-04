from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView, RedirectView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView


from awards.models import Project
from albums.models import Photo
from general.models import UserProfile


from .forms import (SearchForm, BuildForm, BuildFormForum, EditBuildForm, 
                    buildphoto_formfield_callback)
from .models import Build, BuildPhoto
from .utils import get_search_queryset


import json


""" Views responsible for displaying data """


class BuildDetailView(DetailView):
    context_object_name = 'build'
    template_name = 'builds/build.html'
    model = Build

    def get_context_data(self, **kwargs):
        kwargs['photos'] = self.object.buildphoto_set.all().order_by('order', 'id')
        return super(BuildDetailView, self).get_context_data(**kwargs)



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


class AjaxSearchView(View):
    """ 
    Ajax search form suitable for jQuery-ui's 
    autocomplete.
    """

    field_for_value = 'id'
    field_for_label = 'title'

    def get(self, request, *args, **kwargs):
        objects = get_search_queryset(request, key='term')

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

def index_and_add(request):
    """ 
    The index page displays a search field and list of recently added build
    reports. Additionally, logged in users see a form to add new builds.

    This is a rather complex view, due to the formset stuff and two different
    forms. Another form is used to pre-populate the add-form based on GET data,
    coming from the forum.

    TODO: write tests!
    """

    user_logged_in = request.user.is_authenticated()

    # initialize some defaults
    form_kwargs, context = {}, {}
    builds = None
    photos_formset, form = None, None
    
    searchform = SearchForm()
    

    if user_logged_in:
        def formfield_callback(field, **kwargs):
            """ Callback function to limit the photos that can be selected. """
            return buildphoto_formfield_callback(field, request, **kwargs)

        # Initialize the FormSet factory with the correct callback
        BuildPhotoInlineFormSet = inlineformset_factory(
                                      Build, BuildPhoto, 
                                      max_num = 10, extra = 10, 
                                      can_delete = False,
                                      formfield_callback = formfield_callback
                                      )
        photos_formset = BuildPhotoInlineFormSet(queryset=BuildPhoto.objects.none())
    
    
    # Actuall request processing ###############################################
    if user_logged_in and request.method == 'POST':
        form = BuildForm(data=request.POST)
        if form.is_valid():
            build = form.save(commit=False)
            photos_formset = BuildPhotoInlineFormSet(data=request.POST, instance=build)

            if photos_formset.is_valid():
                # commit the changes
                build.user = request.user
                build.profile = request.user.get_profile()
                build.save()
                photos_formset.save()
                return redirect(build.get_absolute_url())
        else:
            photos_formset = BuildPhotoInlineFormSet(data=request.POST, instance=Build())

    else: # GET
        # See if we can fill in some data already from the querystring
        if user_logged_in and 'prefill' in request.GET:
            prefill_form = BuildFormForum(request, request.GET)
            if prefill_form.is_valid():
                form_kwargs['instance'] = prefill_form.get_build()

        # show the search results
        if 'search-button' in request.GET:
            searchform = SearchForm(request.GET)
            if searchform.is_valid():
                builds = get_search_queryset(request, searchform)
            
        
        if user_logged_in:
            form = BuildForm(**form_kwargs)
    
    
    # Populate the context #####################################################
    context['searchform'] = searchform
    context['form'] = form
    context['photos_formset'] = photos_formset

    if builds is None:
        context['builds'] = Build.objects.all().select_related(
                            'user', 'profile', 'brand'
                            ).order_by('-pk')[:20] # TODO: paginate
    else:
        context['builds'] = builds
    
    return render(request, 'builds/add.html', context)

from functools import partial

class BuildUpdate(UpdateView): # TODO
    form_class = EditBuildForm
    template_name = 'builds/edit.html'

    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """ Callback function to limit the photos that can be selected. """
        request = kwargs.pop('request', None)
        return buildphoto_formfield_callback(db_field, request, **kwargs)
    

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_queryset(self):
        if self.request.user.has_perms('builds.edit_build'):
            return Build.objects.all()
        return Build.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        
        BuildPhotoInlineFormSet = inlineformset_factory(Build, BuildPhoto, 
                                    exclude = ('order',),
                                    extra=10, max_num=10,
                                    formfield_callback = partial(
                                        self.formfield_for_dbfield, 
                                        request=self.request
                                        )
                                    )



        kwargs['builds'] = Build.objects.filter(
                                user = self.request.user
                            ).select_related(
                                'user', 'profile', 'brand'
                            ).order_by('-pk')[:20]
        
        kwargs['searchform'] = SearchForm()
        if not kwargs.get('photos_formset', False):
            kwargs['photos_formset'] = BuildPhotoInlineFormSet(instance=self.object)
        return super(BuildUpdate, self).get_context_data(**kwargs)

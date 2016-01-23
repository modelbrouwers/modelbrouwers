from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.detail import SingleObjectMixin

from extra_views import (
    CreateWithInlinesView, InlineFormSet, NamedFormsetsMixin,
    UpdateWithInlinesView
)

from brouwers.general.models import UserProfile
from brouwers.utils.views import LoginRequiredMixin
from .forms import BuildForm, BuildPhotoForm
from .models import Build, BuildPhoto


User = get_user_model()


# TODO: search


class IndexView(ListView):
    photo_qs = BuildPhoto.objects.select_related('photo').order_by('order')
    queryset = Build.objects.select_related('user').prefetch_related(
                    'kits__brand', 'kits__scale',
                    Prefetch('photos', queryset=photo_qs)
               ).order_by('-pk')
    paginate_by = 24
    context_object_name = 'builds'
    show_user = True


class UserBuildListView(IndexView):
    context_object_name = 'builds'
    template_name = 'builds/profile.html'
    show_user = False

    def get_queryset(self):
        qs = super(UserBuildListView, self).get_queryset()
        user_id = self.kwargs.get('user_id', None)
        self.user = get_object_or_404(User, pk=user_id)
        return qs.filter(user_id=user_id)

    def get_context_data(self, **kwargs):
        context = super(UserBuildListView, self).get_context_data(**kwargs)
        context['builds_user'] = self.user
        return context


class BuildDetailView(DetailView):
    model = Build
    context_object_name = 'build'

    def get_context_data(self, **kwargs):
        kwargs['photos'] = self.object.photos.select_related('photo').order_by('order', 'id')
        kwargs['kits'] = list(self.object.kits.select_related('brand', 'scale'))
        return super(BuildDetailView, self).get_context_data(**kwargs)


class BuildRedirectView(SingleObjectMixin, RedirectView):
    """
    Get the build by pk, redirect to the slug url
    """
    model = Build
    permanent = True

    def get_redirect_url(self, **kwargs):
        return self.get_object().get_absolute_url()


class ProfileRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs):
        profile_id = self.kwargs.get('profile_id', None)
        profile = get_object_or_404(UserProfile, pk=profile_id)
        return reverse('builds:user_build_list', kwargs={'user_id': profile.user.id})


class PhotoInline(InlineFormSet):
    model = BuildPhoto
    form_class = BuildPhotoForm
    extra = 0  # all done dynamically

    # TODO: patch extra_views.formsets.BaseInlineFormSetMixin.get_factory_kwargs
    # do not set self.fields if self.form_class is provided
    def get_factory_kwargs(self):
        kwargs = super(PhotoInline, self).get_factory_kwargs()
        del kwargs['fields']
        return kwargs


class BuildCreateView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Build
    form_class = BuildForm
    inlines = [PhotoInline]
    inlines_names = ['photos']

    def forms_valid(self, form, inlines):
        form.instance.user = self.request.user
        return super(BuildCreateView, self).forms_valid(form, inlines)


class BuildUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Build
    form_class = BuildForm
    inlines = [PhotoInline]
    inlines_names = ['photos']

    def get_queryset(self):
        # TODO: object-level permissions?
        qs = super(BuildUpdateView, self).get_queryset()
        return qs.filter(user=self.request.user)

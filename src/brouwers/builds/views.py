from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.detail import SingleObjectMixin

from extra_views import (
    CreateWithInlinesView, InlineFormSetFactory, NamedFormsetsMixin,
    UpdateWithInlinesView
)

from brouwers.forum_tools.models import ForumUser
from brouwers.general.models import UserProfile
from brouwers.utils.views import LoginRequiredMixin

from .forms import BuildForm, BuildPhotoForm, BuildSearchForm
from .models import Build, BuildPhoto

User = get_user_model()


class BuildSearchMixin(object):

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = BuildSearchForm(auto_id=False)
        return super().get_context_data(**kwargs)


class IndexView(BuildSearchMixin, ListView):
    photo_qs = BuildPhoto.objects.select_related('photo').order_by('order')
    queryset = (
        Build.objects
        .select_related('user')
        .prefetch_related(
            'kits__brand',
            'kits__scale',
            Prefetch('photos', queryset=photo_qs)
        )
        .order_by('-pk')
    )
    paginate_by = 24
    context_object_name = 'builds'
    show_user = True


class UserBuildListView(IndexView):
    context_object_name = 'builds'
    template_name = 'builds/profile.html'
    show_user = False

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.kwargs.get('user_id', None)
        self.user = get_object_or_404(User, pk=user_id)
        return qs.filter(user_id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['builds_user'] = self.user
        return context


class BuildDetailView(BuildSearchMixin, DetailView):
    model = Build
    context_object_name = 'build'

    def get_context_data(self, **kwargs):
        kwargs['photos'] = self.object.photos.select_related('photo').order_by('order', 'id')
        kwargs['kits'] = list(self.object.kits.select_related('brand', 'scale'))
        return super().get_context_data(**kwargs)


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


class ForumUserRedirectView(SingleObjectMixin, RedirectView):
    """
    Takes the forumuser pk and redirects to the associated user's profile.
    """
    permanent = True
    model = ForumUser

    def get_redirect_url(self, **kwargs):
        forum_user = self.get_object()
        try:
            user = User.objects.get_from_forum(forum_user)
        except User.DoesNotExist:
            raise Http404
        return reverse('builds:user_build_list', kwargs={'user_id': user.id})


class PhotoInline(InlineFormSetFactory):
    model = BuildPhoto
    form_class = BuildPhotoForm
    factory_kwargs = {
        "extra": 0,
    }

    # TODO: patch extra_views.formsets.BaseInlineFormSetFactory.get_factory_kwargs
    # do not set self.fields if self.form_class is provided
    def get_factory_kwargs(self):
        kwargs = super().get_factory_kwargs()
        del kwargs['fields']
        return kwargs


class BuildCreateView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Build
    form_class = BuildForm
    inlines = [PhotoInline]
    inlines_names = ['photos']

    def get_initial(self):
        initial = {
            'title': self.request.GET.get('title', ''),
            'topic': self.request.GET.get('topic_id', ''),
        }
        return initial

    def forms_valid(self, form, inlines):
        form.instance.user = self.request.user
        return super().forms_valid(form, inlines)


class BuildUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Build
    form_class = BuildForm
    inlines = [PhotoInline]
    inlines_names = ['photos']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

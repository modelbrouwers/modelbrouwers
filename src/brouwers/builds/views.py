from functools import partial
import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db.models import Prefetch
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView

from extra_views import CreateWithInlinesView, InlineFormSet, NamedFormsetsMixin

from brouwers.general.models import UserProfile
from brouwers.utils.views import LoginRequiredMixin
from .forms import BuildForm, BuildPhotoForm
from .models import Build, BuildPhoto


User = get_user_model()


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
    extra = 3

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

    def get_success_url(self):
        return self.object.get_absolute_url()






# class BuildUpdate(UpdateView):
#     form_class = BuildForm
#     template_name = 'builds/edit.html'

#     def get_queryset(self):
#         if self.request.user.has_perms('builds.edit_build'):
#             return Build.objects.all()
#         return Build.objects.filter(user_id=self.request.user.id)

#     def formfield_for_dbfield(self, db_field, **kwargs):
#         """ Callback function to limit the photos that can be selected. """
#         request = kwargs.pop('request', None)
#         return buildphoto_formfield_callback(db_field, request, **kwargs)

#     def get_formset_class(self):
#         ff_callback = partial(self.formfield_for_dbfield, request=self.request)
#         return inlineformset_factory(Build, BuildPhoto,
#                                     exclude = ('order',),
#                                     extra=10, max_num=10,
#                                     formfield_callback = ff_callback,
#                                     can_delete = True
#                                     )

#     def get_success_url(self):
#         """ Show the detail page """
#         return self.object.get_absolute_url()

#     def get_formset(self, **kwargs):
#         """ Method to easily get the formset in different stages """
#         BuildPhotoFormset = self.get_formset_class()
#         return BuildPhotoFormset(**kwargs)

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         formset = self.get_formset(instance=self.object, data=self.request.POST)
#         if formset.is_valid():
#             self.object.save()
#             formset.save()
#             return redirect(self.get_success_url())
#         else:
#             return self.form_invalid(form, formset=formset)

#     def form_invalid(self, form, formset=None):
#         context = {'form': form}
#         if formset is not None:
#             context['photos_formset'] = formset
#         else:
#             formset = self.get_formset(instance=self.object, data=self.request.POST)
#             # trigger validation
#             formset.is_valid()
#             context['photos_formset'] = formset
#         return self.render_to_response(self.get_context_data(**context))

#     def get_context_data(self, **context):

#         context['builds'] = Build.objects.filter(
#                                 user = self.request.user
#                             ).select_related(
#                                 'user', 'profile', 'brand'
#                             ).order_by('-pk')[:20]

#         context['searchform'] = SearchForm()

#         if not context.get('photos_formset', False):
#             context['photos_formset'] = self.get_formset(instance=self.object)

#         # get the image urls for each photo
#         photos_data = {}
#         for photo in self.object.buildphoto_set.select_related('photo').exclude(photo_id=None):
#             photos_data[photo.photo.id] = photo.image_url
#             context['photo_urls'] = json.dumps(photos_data)

#         return super(BuildUpdate, self).get_context_data(**context)

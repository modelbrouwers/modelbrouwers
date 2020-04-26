from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, TemplateView, UpdateView
)

from brouwers.utils.views import LoginRequiredMixin

from ..forms import (
    AlbumForm, AlbumRestoreForm, PhotoForm, PhotoRestoreForm, PreferencesForm,
    UploadForm
)
from ..models import Album, Photo, Preferences


class UploadView(LoginRequiredMixin, TemplateView):
    template_name = 'albums/upload.html'

    def get(self, request, *args, **kwargs):
        if not request.user.album_set.exists():
            messages.warning(request, _('You need to create an album before you can upload photos'))
            return redirect(reverse('albums:create'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = UploadForm(self.request, initial=self.request.GET)
        kwargs['settings'] = Preferences.objects.get_for(self.request.user)
        return super().get_context_data(**kwargs)


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album/create.html'
    success_url = reverse_lazy('albums:upload')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial.setdefault('title', "album %s" % timezone.now().strftime("%d-%m-%Y"))
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        url = super().get_success_url()
        return u'%s%s' % (url, '?album=%s' % self.object.id)


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album/update.html'
    success_url = reverse_lazy('albums:mine')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = 'albums/album/confirm_delete.html'
    context_object_name = 'album'
    success_url = reverse_lazy('albums:mine')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs['photos'] = self.object.photo_set.filter(trash=False)
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.trash = True
        self.object.save()
        restore_url = reverse('albums:restore', kwargs={'pk': self.object.pk})
        messages.success(request, _('The album was deleted. <a href="{0}">Undo</a>').format(restore_url))
        return redirect(success_url)


class AlbumRestoreView(AlbumUpdateView):
    form_class = AlbumRestoreForm
    success_url = reverse_lazy('albums:mine')
    template_name = 'albums/album/restore.html'
    initial = {
        'trash': False,
    }


class PhotoSuccessURLMixin(object):
    def get_success_url(self):
        if not self.object.trash:
            return self.object.get_absolute_url()
        return reverse('albums:detail', kwargs={'pk': self.object.album.pk})


class PhotoUpdateView(PhotoSuccessURLMixin, LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo/update.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'albums/photo/confirm_delete.html'
    context_object_name = 'photo'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user, trash=False)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.trash = True
        self.object.save()
        restore_url = reverse('albums:photo_restore', kwargs={'pk': self.object.pk})
        messages.success(request, _('The photo was deleted. <a href="{0}">Undo</a>').format(restore_url))
        return redirect(success_url)

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.object.album.pk})


class PhotoRestoreView(PhotoSuccessURLMixin, LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoRestoreForm
    template_name = 'albums/photo/restore.html'
    initial = {
        'trash': False,
    }

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class PreferencesUpdateView(LoginRequiredMixin, UpdateView):
    model = Preferences
    form_class = PreferencesForm
    success_url = reverse_lazy('albums:index')

    def get_object(self, queryset=None):
        obj, _ = Preferences.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('The changes have been saved.'))
        return response

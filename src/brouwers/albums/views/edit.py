from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from brouwers.utils.views import LoginRequiredMixin
from ..forms import AlbumForm, AlbumRestoreForm, PreferencesForm, UploadForm
from ..models import Album, Preferences


class UploadView(LoginRequiredMixin, TemplateView):
    template_name = 'albums/upload.html'

    def get(self, request, *args, **kwargs):
        if not request.user.album_set.exists():
            messages.warning(request, _('You need to create an album before you can upload photos'))
            return redirect(reverse('albums:create'))
        return super(UploadView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = UploadForm(self.request, initial=self.request.GET)
        kwargs['settings'] = Preferences.objects.get_for(self.request.user)
        return super(UploadView, self).get_context_data(**kwargs)


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/create.html'
    success_url = reverse_lazy('albums:upload')

    def get_initial(self):
        initial = super(AlbumCreateView, self).get_initial()
        initial.setdefault('title', "album %s" % timezone.now().strftime("%d-%m-%Y"))
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AlbumCreateView, self).form_valid(form)

    def get_success_url(self):
        url = super(AlbumCreateView, self).get_success_url()
        return u'%s%s' % (url, '?album=%s' % self.object.id)


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/update.html'
    success_url = reverse_lazy('albums:mine')

    def get_queryset(self):
        qs = super(AlbumUpdateView, self).get_queryset()
        return qs.filter(user=self.request.user)


class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    context_object_name = 'album'
    success_url = reverse_lazy('albums:mine')

    def get_queryset(self):
        qs = super(AlbumDeleteView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs['photos'] = self.object.photo_set.filter(trash=False)
        return super(AlbumDeleteView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.trash = True
        self.object.save()
        messages.success(request, _('The album was deleted'))
        return redirect(success_url)


class AlbumRestoreView(AlbumUpdateView):
    form_class = AlbumRestoreForm
    success_url = reverse_lazy('albums:mine')
    template_name = 'albums/restore.html'
    initial = {
        'trash': False,
    }


class PreferencesUpdateView(LoginRequiredMixin, UpdateView):
    model = Preferences
    form_class = PreferencesForm
    success_url = reverse_lazy('albums:index')

    def get_object(self, queryset=None):
        obj, _ = Preferences.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        response = super(PreferencesUpdateView, self).form_valid(form)
        messages.success(self.request, _('The changes have been saved.'))
        return response

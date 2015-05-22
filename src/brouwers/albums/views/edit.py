from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView

from brouwers.utils.views import LoginRequiredMixin
from ..forms import CreateAlbumForm, PreferencesForm, UploadForm
from ..models import Album, Preferences


class UploadView(LoginRequiredMixin, TemplateView):
    template_name = 'albums/upload.html'

    def get(self, request, *args, **kwargs):
        if not request.user.album_set.exists():
            messages.warning(request, _('You need to create an album before you can upload photos'))
            return redirect(reverse('albums:create'))
        return super(UploadView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = UploadForm(self.request)
        return super(UploadView, self).get_context_data(**kwargs)


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = CreateAlbumForm
    template_name = 'albums/create.html'
    success_url = reverse_lazy('albums:upload')

    def get_initial(self):
        initial = super(AlbumCreateView, self).get_initial()
        initial.setdefault('title', "album %s" % timezone.now().strftime("%d-%m-%Y"))
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AlbumCreateView, self).form_valid(form)


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

from collections import OrderedDict

from django.views.generic import TemplateView

from brouwers.utils.views import LoginRequiredMixin
from ..models import Album


class MyAlbumsView(LoginRequiredMixin, TemplateView):

    template_name = 'albums/my_albums.html'

    def get_queryset(self, **extra_filters):
        return self.request.user.album_set.filter(trash=False, **extra_filters)

    def get_shared_albums(self):
        user = self.request.user
        return Album.objects.filter(albumgroup__users=user)

    def get_my_shared_albums(self):
        user = self.request.user
        return user.album_set.exclude(albumgroup__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(MyAlbumsView, self).get_context_data(**kwargs)
        tab_order = ['public', 'private', 'shared-with-me', 'shared-by-me']
        _tab_content = {
            'public': self.get_queryset(public=True),
            'private': self.get_queryset(public=False),
            'shared-with-me': self.get_shared_albums(),
            'shared-by-me': self.get_my_shared_albums(),
        }
        context['tabcontent'] = OrderedDict(sorted(_tab_content.items(), key=lambda t: tab_order.index(t[0])))
        return context

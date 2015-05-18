import random

from django.db.models import F, Q
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from brouwers.awards.models import Nomination
from ..models import Album, Photo


class IndexView(ListView):
    queryset = Album.objects.for_index()
    template_name = 'albums/index.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_awards_winners(self):
        awards_winners = Nomination.objects.winners()
        try:
            awards_winners = random.sample(awards_winners, 3)
        except ValueError:  # sample greater than population, use entire set
            pass
        return awards_winners

    def get_context_data(self, **kwargs):
        # spotlight: awards winners, select 3 random categories
        # kwargs['awards_winners'] = self.get_awards_winners()
        kwargs['latest_uploads'] = Photo.objects.select_related('user').filter(
                                       album__public=True).order_by('-uploaded')[:20]
        return super(IndexView, self).get_context_data(**kwargs)


class AlbumDetailView(ListView, SingleObjectMixin):
    paginate_by = 24
    object = None  # SingleObjectMixin
    context_object_name = 'photos'
    template_name = 'albums/album_detail.html'

    def get(self, request, *args, **kwargs):
        album = self.get_album()
        album.views = F('views') + 1
        album.save()
        self.get_album(refresh=True)
        return super(AlbumDetailView, self).get(request, *args, **kwargs)

    def get_album(self, refresh=False):
        if self.object is None or refresh:
            self.object = self.get_object(queryset=self.get_album_queryset())
        return self.object

    def get_album_queryset(self):
        qs = Album.objects.public()
        if self.request.user.is_authenticated():
            groups = self.request.user.albumgroup_set.all()
            qs2 = Album.objects.filter(Q(user=self.request.user) | Q(albumgroup__in=groups))
            return (qs | qs2).distinct()
        return qs

    def get_queryset(self):
        """
        Fetch the album from the url and retrieve the photo_set to build the
        list view.
        """
        return self.get_album().photo_set.filter(trash=False)

    def get_context_data(self, **kwargs):
        kwargs['album'] = self.get_album()
        return super(AlbumDetailView, self).get_context_data(**kwargs)

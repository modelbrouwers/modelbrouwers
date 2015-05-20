import random

from django.db.models import F, Q
from django.views.generic import ListView, DetailView, RedirectView
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


class AlbumListRedirectView(RedirectView):
    pattern_name = 'albums:list'


class AlbumListView(ListView):
    queryset = Album.objects.for_index()
    context_object_name = 'albums'
    paginate_by = 16


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


class PhotoDetailView(DetailView):
    queryset = Photo.objects.filter(trash=False, album__trash=False).select_related('user', 'album')

    def get_queryset(self):  # TODO: test
        qs = super(PhotoDetailView, self).get_queryset()
        user = self.request.user
        if not user.is_authenticated():
            qs = qs.filter(album__public=True)
        else:
            qs = qs.filter(Q(user=user) | Q(album__albumgroup__users=user))
        return qs

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views = F('views') + 1
        obj.save()
        return super(PhotoDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        context.update({
            'next': Photo.objects.next(self.object, user=self.request.user),
            'previous': Photo.objects.previous(self.object, user=self.request.user)
        })
        return context

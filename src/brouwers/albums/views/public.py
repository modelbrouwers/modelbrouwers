import logging
import os

# import random
import zipfile

from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, Q
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from django_sendfile import sendfile

# from brouwers.awards.models import Nomination
from brouwers.utils.views import LoginRequiredMixin

from ..models import ALBUM_SEARCH_VECTOR, Album, AlbumDownload, Photo

logger = logging.getLogger(__name__)


class AlbumQuerysetMixin(object):
    queryset = Album.objects.public()

    def get_album_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            groups = self.request.user.albumgroup_set.all()
            qs2 = Album.objects.filter(
                Q(user=self.request.user) | Q(albumgroup__in=groups)
            )
            return (qs | qs2).distinct()
        return qs


class IndexView(ListView):
    queryset = Album.objects.for_index()
    template_name = "albums/index.html"
    context_object_name = "albums"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        kwargs["latest_uploads"] = (
            Photo.objects.select_related("user")
            .filter(
                trash=False,
                album__public=True,
                album__trash=False,
            )
            .order_by("-uploaded")[:20]
        )
        return super().get_context_data(**kwargs)


class SearchView(ListView):
    queryset = Album.objects.public().select_related("user", "cover")
    template_name = "albums/album/search_results.html"
    context_object_name = "albums"
    paginate_by = 16

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if not query:
            return qs.none()

        rank = SearchRank(
            vector=ALBUM_SEARCH_VECTOR, query=SearchQuery(query, config="dutch")
        )
        qs = (
            qs.annotate(rank=rank)
            .filter(Q(rank__gte=0.1) | Q(user__username__icontains=query))
            .order_by("-rank")
        )

        return qs


class AlbumListView(ListView):
    queryset = Album.objects.for_index()
    template_name = "albums/album/list.html"
    context_object_name = "albums"
    paginate_by = 16


class AlbumDetailView(AlbumQuerysetMixin, ListView, SingleObjectMixin):
    paginate_by = 24
    object = None  # SingleObjectMixin
    template_name = "albums/album/detail.html"
    context_object_name = "photos"

    def get(self, request, *args, **kwargs):
        album = self.get_album()
        album.views = F("views") + 1
        album.save()
        self.get_album(refresh=True)
        return super().get(request, *args, **kwargs)

    def get_album(self, refresh=False):
        if self.object is None or refresh:
            self.object = self.get_object(queryset=self.get_album_queryset())
        return self.object

    def get_queryset(self):
        """
        Fetch the album from the url and retrieve the photo_set to build the
        list view.
        """
        return self.get_album().photo_set.filter(trash=False)

    def get_context_data(self, **kwargs):
        kwargs["album"] = self.get_album()
        return super().get_context_data(**kwargs)


class AlbumDownloadView(LoginRequiredMixin, AlbumQuerysetMixin, DetailView):
    def get_queryset(self):
        return self.get_album_queryset()

    def get(self, request, *args, **kwargs):
        album = self.get_object()
        reuse_zip = AlbumDownload.objects.filter(
            album=album, timestamp__gte=album.last_upload, failed=False
        ).exists()

        filename = os.path.join(
            settings.SENDFILE_ROOT,
            "albums",
            str(album.user_id),
            str(album.id),
            "{}.zip".format(album.id),
        )

        if not reuse_zip:
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            download = AlbumDownload.objects.create(
                album=album, downloader=request.user, failed=True
            )
            with zipfile.ZipFile(filename, "w") as ziph:
                for photo in album.photo_set.filter(trash=False):
                    if not photo.exists:
                        logger.warn("Missing photo: %d" % photo.id)
                        continue
                    image = photo.image.path
                    ziph.write(image, os.path.split(image)[1])

            download.failed = False
            download.save()

        return sendfile(request, filename, attachment=True)


class PhotoDetailView(DetailView):
    queryset = Photo.objects.filter(trash=False, album__trash=False).select_related(
        "user", "album"
    )
    template_name = "albums/photo/detail.html"

    def get_queryset(self):  # TODO: test
        qs = super().get_queryset()
        user = self.request.user
        q = Q(album__public=True)
        if user.is_authenticated:
            q |= Q(user=user) | Q(album__albumgroup__users=user)
        return qs.filter(q)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views = F("views") + 1
        obj.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "next": Photo.objects.next(self.object, user=self.request.user),
                "previous": Photo.objects.previous(self.object, user=self.request.user),
            }
        )
        return context

from django.conf.urls import patterns, url
from django.views.generic import RedirectView

# from .ajax_views import RotateView
from .views import (
    IndexView, AlbumListView, AlbumDetailView, PhotoDetailView,
    UploadView, AlbumCreateView, AlbumDownloadView, PreferencesUpdateView,
    MyAlbumsView
)


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^new/$', AlbumCreateView.as_view(), name='create'),
    url(r'^list/$', RedirectView.as_view(pattern_name='albums:all', permanent=True)),
    url(r'^all/$', AlbumListView.as_view(), name='all'),
    url(r'^mine/$', MyAlbumsView.as_view(), name='mine'),
    url(r'^my_gallery/$', RedirectView.as_view(pattern_name='albums:mine', permanent=True)),
    url(r'^album/\{?(?P<pk>\d+)\}?/$', AlbumDetailView.as_view(), name='detail'),  # curly braces for Javascript url
    url(r'^album/(?P<pk>\d+)/page/(?P<page>\d+)/$', AlbumDetailView.as_view(), name='detail'),
    url(r'^album/(?P<pk>\d+)/download/$', AlbumDownloadView.as_view(), name='download'),
    url(r'^photo/(?P<pk>\d+)/$', PhotoDetailView.as_view(), name='photo-detail'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^settings/$', PreferencesUpdateView.as_view(), name='settings'),
    url(r'^preferences/$', RedirectView.as_view(pattern_name='albums:settings', permanent=True)),
)

# AJAX -> convert to API?
urlpatterns += patterns(
    'brouwers.albums.ajax_views',
    # (r'^upload/from_url/$',     'upload_url'),
    # url(r'^photo/(?P<pk>\d+)/rotate/', login_required(RotateView.as_view()), name='rotate_photo'),
)

# TODO: convert to api
urlpatterns += patterns(
    'brouwers.albums.ajax_views_forum',
    (r'^get_photos/(\d+)/$',    'get_photos'),
    (r'^is_beta_tester/$',      'is_beta_tester'),
    (r'^search_own_albums/$',   'search'),
    (r'^sidebar/$',             'get_sidebar'),
    (r'^sidebar_options/$',     'get_sidebar_options'),
)

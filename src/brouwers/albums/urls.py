from django.conf import settings
from django.conf.urls import *
from django.contrib.auth.decorators import login_required

from .ajax_views import RotateView

urlpatterns = patterns('brouwers.albums.views',
    (r'^$', 'index'),
    (r'^album/(\d+)/$',     'browse_album'),
    (r'^album/(\d+)/edit/', 'edit_album'),
    (r'^album/(\d+)/download/', 'download_album'),
    (r'^list/$',             'albums_list'), #all albums
    (r'^manage/(\d+)/$',    'manage'),
    (r'^my_gallery/$',      'my_albums_list'),
    (r'^my_gallery/last_uploads/$', 'my_last_uploads'),
    (r'^photo/(\d+)/$',     'photo'),
    (r'^photo/(\d+)/edit/$','edit_photo'),
    (r'^preferences/$',     'preferences'),
    (r'^upload/$',          'uploadify'),
    (r'^upload/basic/$',    'upload'),
    (r'^upload/extra_info/$', 'set_extra_info'),
    (r'^upload/uploadify/complete/$', 'pre_extra_info_uploadify'),
    (r'^manage/$',          'manage'),
)

# AJAX
urlpatterns += patterns('brouwers.albums.ajax_views',
    (r'^album/edit/$',          'edit_album'),
    (r'^album/get_covers/$',    'get_covers'),
    (r'^album/get_title/$',     'get_title'),
    (r'^album/group_rights/$',  'edit_albumgroup'),
    (r'^album/new/$',           'new_album_jquery_ui'),
    (r'^album/remove/$',        'remove_album'),
    (r'^album/restore/$',       'restore_album'),
    (r'^all_own/$',             'get_all_own_albums'),
    (r'^new_album/$',           'new_album'),
    (r'^photo/delete',          'delete_photo'),
    url(r'^photo/(?P<pk>\d+)/rotate', login_required(RotateView.as_view()), name='rotate_photo'),
    (r'^upload/uploadify/$',    'uploadify'),
    (r'^upload/from_url/$',     'upload_url'),
    (r'^reorder/$',             'reorder'),
    (r'^search/$',              'search'),
    (r'^set_cover/$',           'set_cover'),
)

urlpatterns += patterns('brouwers.albums.ajax_views_forum',
    (r'^get_photos/(\d+)/$',    'get_photos'),
    (r'^is_beta_tester/$',      'is_beta_tester'),
    (r'^search_own_albums/$',   'search'),
    (r'^sidebar/$',             'get_sidebar'),
    (r'^sidebar_options/$',     'get_sidebar_options'),
)

# API
if 'tastypie' in settings.INSTALLED_APPS:
    from tastypie.api import Api
    from brouwers.albums.api.resources import AlbumResource, OwnAlbumsResource, PhotoResource

    v1_api = Api(api_name='v1')

    v1_api.register(AlbumResource())
    v1_api.register(OwnAlbumsResource())
    v1_api.register(PhotoResource())

    urlpatterns += patterns('',
        url(r'^api/', include(v1_api.urls)),
    )

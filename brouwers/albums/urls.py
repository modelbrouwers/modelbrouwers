from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.albums.views',
    (r'^$', 'index'),
    (r'^album/(\d+)/$',     'browse_album'),
    (r'^album/(\d+)/edit/', 'edit_album'),
    (r'^list/$',             'albums_list'), #all albums
    (r'^manage/(\d+)/$',    'manage'),
    (r'^my_gallery/$',      'my_albums_list'),
    (r'^my_gallery/last_uploads/$', 'my_last_uploads'),
    (r'^photo/(\d+)/$',     'photo'),
    (r'^photo/(\d+)/edit/$','edit_photo'),
    (r'^photos/$',          'photos'),
    (r'^preferences/$',     'preferences'),
    (r'^upload/$',          'uploadify'),
    (r'^upload/basic/$',    'upload'),
    (r'^upload/extra_info/$', 'set_extra_info'),
    (r'^upload/uploadify/complete/$', 'pre_extra_info_uploadify'),
    (r'^manage/$',          'manage'),
    )

# AJAX
urlpatterns += patterns('brouwers.albums.ajax_views',
    (r'^all_own/$',             'get_all_own_albums'),
    (r'^new_album/$',           'new_album'),
    (r'^upload/uploadify/$',    'uploadify'),
    (r'^reorder/$',             'reorder'),
    (r'^search/$',              'search'),
    (r'^set_cover/$',           'set_cover'),
    )

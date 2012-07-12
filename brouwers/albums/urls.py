from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.albums.views',
	(r'^$', 'index'),
	(r'^upload/$', 'upload_flash'),
	(r'^upload/basic/$', 'upload'),
	(r'^upload/extra_info/$', 'set_extra_info'),
	(r'^upload/uploadify/$', 'uploadify'),
	(r'^upload/uploadify/complete/$', 'pre_extra_info_uploadify'),
	(r'^manage/$', 'manage'),
	(r'^manage/(\d+)/$', 'manage'),
	(r'^photos/$', 'photos'),
    )

# AJAX
urlpatterns += patterns('brouwers.albums.ajax_views',
    (r'^new_album/$', 'new_album'),
    )

from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.albums.views',
	(r'^$', 'index'),
	(r'^upload/$', 'upload'),
	(r'^upload/extra_info/$', 'set_extra_info'),
	(r'^manage/$', 'manage'),
	(r'^manage/(\d+)/$', 'manage'),
    )

from django.conf.urls.defaults import *

# Everything is AJAX
urlpatterns = patterns('forum_tools.views',
	(r'^get_sync_data/$', 'get_sync_data'),
	)

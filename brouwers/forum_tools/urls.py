from django.conf.urls.defaults import *

# Everything is AJAX
urlpatterns = patterns('forum_tools.views',
	(r'^get_sync_data/$',  'get_sync_data'),
	(r'^get_chat/$',       'get_chat'),
    (r'^get_post_perm/$',  'get_posting_level'),
	(r'^mods/get_data/$',  'get_mod_data'),
    (r'^mods/get_sharing_perms/$', 'get_sharing_perms'),
	)

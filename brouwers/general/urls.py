from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.general.views',
#    (r'^$', 'index'),
    (r'^login/$', 'custom_login'),
    (r'^logout/$', 'custom_logout'),
    (r'^register/$', 'register'),
    (r'^profile/$', 'profile'),
    (r'^users/(\w+)/$', 'user_profile'),
    (r'^confirm_account/$', 'confirm_account'),
    )

urlpatterns += patterns('django.contrib.auth.views',
    (r'^profile/change_password/$', 'password_change', {'template_name':'general/password.html'}),
    (r'^password_change_done/$','password_change_done', {'template_name': 'general/password_change_done.html'}),
    )

if not settings.DEVELOPMENT:
	urlpatterns += patterns('django.views.generic.simple',
	#    (r'^$', 'direct_to_template', {'template': 'base.html'}),
		(r'^$', 'redirect_to', {'url': '/index.php'}),
		)
else:
	urlpatterns += patterns('brouwers.general.views',
    	(r'^$', 'index'),
    )

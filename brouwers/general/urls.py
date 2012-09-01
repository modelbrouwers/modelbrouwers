from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'base.html'}),
#    (r'^phpBB3/$', 'redirect_to', {'url': 'http://localhost/phpBB3/'}),
    )

urlpatterns += patterns('brouwers.general.views',
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

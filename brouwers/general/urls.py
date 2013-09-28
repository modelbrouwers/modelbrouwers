from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('general.views',
    (r'^$', 'index'),
    (r'^login/$', 'custom_login'),
    (r'^logout/$', 'custom_logout'),
    (r'^register/$', 'register'),
    (r'^profile/$', 'profile'),
    (r'^users/(\w+)/$', 'user_profile'),
    (r'^confirm_account/$', 'confirm_account'),
    (r'^reset_pw/$', 'password_reset'),
    (r'^do_reset_pw/$', 'do_password_reset'),
    )

# new auth backend
urlpatterns += patterns('general.views2',
    (r'^new_login/$',     'custom_login'),
    )

# AJAX
urlpatterns += patterns('general.ajax_views',
    (r'^user/search/$',    'search_users'),
    (r'^profile/ajax/change_password/$', 'password_change'),
    )

urlpatterns += patterns('django.contrib.auth.views',
    (r'^profile/change_password/$', 'password_change', {'template_name':'general/password.html'}),
    (r'^password_change_done/$','password_change_done', {'template_name': 'general/password_change_done.html'}),
    )

# API
if 'tastypie' in settings.INSTALLED_APPS:
    from tastypie.api import Api
    from general.api.resources import UserResource

    v1_api = Api(api_name='v1')

    v1_api.register(UserResource())

    urlpatterns += patterns('',
        (r'^api/', include(v1_api.urls)),
        )
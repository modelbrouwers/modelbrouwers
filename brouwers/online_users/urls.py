from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.online_users.views',
    (r'^so/$', 'set_online'),
    (r'^ous/$', 'get_online_users')
)

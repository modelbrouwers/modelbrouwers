from django.conf.urls import patterns, url

urlpatterns = patterns('brouwers.online_users.views',
    url(r'^so/$', 'set_online'),
    url(r'^ous/$', 'get_online_users')
)

from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.migration.views',
    (r'^$', 'index'),
    (r'^albumusers/$', 'albumusers'),
    (r'^find_django_user/$', 'find_django_user'),
    )

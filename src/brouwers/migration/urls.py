from django.conf.urls import patterns, url

urlpatterns = patterns('brouwers.migration.views',
    url(r'^$', 'index'),
    url(r'^albumusers/$', 'albumusers'),
    url(r'^find_django_user/$', 'find_django_user'),
    url(r'^migrate_albums/$', 'migrate_albums'),
    url(r'^migrate_pictures/$', 'migrate_pictures'),
)

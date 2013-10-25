from django.conf.urls.defaults import *

urlpatterns = patterns('migration.views',
    (r'^$', 'index'),
    (r'^albumusers/$', 'albumusers'),
    (r'^find_django_user/$', 'find_django_user'),
    (r'^migrate_albums/$', 'migrate_albums'),
    (r'^migrate_pictures/$', 'migrate_pictures'),
    )

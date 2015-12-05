from django.conf.urls import url

from .views import index, albumusers, find_django_user, migrate_albums, migrate_pictures


urlpatterns = [
    url(r'^$', index),
    url(r'^albumusers/$', albumusers),
    url(r'^find_django_user/$', find_django_user),
    url(r'^migrate_albums/$', migrate_albums),
    url(r'^migrate_pictures/$', migrate_pictures),
]

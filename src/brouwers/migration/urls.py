from django.conf.urls import url

from .views import index, albumusers, find_django_user, migrate_albums, migrate_pictures


app_name = 'migration'
urlpatterns = [
    url(r'^$', index),
    url(r'^albumusers/$', albumusers, name='albumusers'),
    url(r'^find_django_user/$', find_django_user, name='find_django_user'),
    url(r'^migrate_albums/$', migrate_albums, name='migrate_albums'),
    url(r'^migrate_pictures/$', migrate_pictures, name='migrate_pictures'),
]

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^groupbuilds/', include('groupbuilds.api.urls', namespace='groupbuilds')),
)

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^groupbuilds/', include('groupbuilds.api.urls', namespace='groupbuilds')),
    url(r'^forum_tools/', include('forum_tools.api.urls', namespace='forum_tools')),
)

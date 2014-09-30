from django.conf.urls import patterns, url

from .views import GroupBuildDetail


urlpatterns = patterns('',
    url(r'^groupbuild/(?P<pk>\d+)/', GroupBuildDetail.as_view(), name='groupbuild-detail'),
    url(r'^groupbuild/(?P<slug>[\w\-_]+)/', GroupBuildDetail.as_view(), name='groupbuild-detail'),
)

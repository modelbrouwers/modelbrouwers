from django.conf.urls import patterns, url

from .views import GroupBuildDetail, GroupBuildParticipantCheckView


urlpatterns = patterns(
    '',
    url(r'^groupbuild/(?P<pk>\d+)/', GroupBuildDetail.as_view(), name='groupbuild-detail'),
    url(r'^groupbuild/(?P<slug>[\w\-_]+)/', GroupBuildDetail.as_view(), name='groupbuild-detail'),
    url(r'^participant/check/$', GroupBuildParticipantCheckView.as_view(), name='participant-check'),
)

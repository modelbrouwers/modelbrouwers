from django.conf.urls import patterns, url

from .views import GroupBuildDetail, GroupBuildParticipantCheckView, ParticipantCreateView


urlpatterns = patterns(
    '',
    url(r'^groupbuild/(?P<pk>\d+)/$', GroupBuildDetail.as_view(), name='groupbuild-detail'),
    url(r'^groupbuild/(?P<slug>[\w\-_]+)/$', GroupBuildDetail.as_view(), name='groupbuild-detail'),
    url(r'^groupbuild/(?P<pk>\d+)/participant/$', ParticipantCreateView.as_view(), name='groupbuild-participant'),
    url(r'^participant/check/$', GroupBuildParticipantCheckView.as_view(), name='participant-check'),
)

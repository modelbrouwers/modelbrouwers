from django.conf.urls import patterns, url

from .views.admin import GroupBuildCreateView, GroupBuildUpdateView, GroupBuildSubmitView
from .views.participant import (GroupBuildParticipateView, ParticipantUpdateView,
                                MyGroupbuildsListView)
from .views.public import GroupBuildListView, GroupBuildDetailView


urlpatterns = patterns('',
    url(r'^$', GroupBuildListView.as_view(), name='groupbuild-list'),
    url(r'^dashboard/$', MyGroupbuildsListView.as_view(), name='dashboard'),
    url(r'^concept/$', GroupBuildCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', GroupBuildDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', GroupBuildUpdateView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/submit/$', GroupBuildSubmitView.as_view(), name='submit'),
    url(r'^(?P<slug>[\w-]+)/participate/$', GroupBuildParticipateView.as_view(), name='participate'),
    url(r'^(?P<slug>[\w-]+)/participant/(?P<pk>\d+)/$',
        ParticipantUpdateView.as_view(), name='update-participant'),
)

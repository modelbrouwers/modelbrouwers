from django.conf.urls import patterns, url

from .views import (GroupBuildListView, GroupBuildCreateView, GroupBuildDetailView,
                    GroupBuildUpdateView)

urlpatterns = patterns('',
    url(r'^$', GroupBuildListView.as_view(), name='groupbuild-list'),
    url(r'^concept/$', GroupBuildCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', GroupBuildDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', GroupBuildUpdateView.as_view(), name='edit'),
)

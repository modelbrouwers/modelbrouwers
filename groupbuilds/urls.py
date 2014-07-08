from django.conf.urls import patterns, url

from .views import GroupBuildListView, GroupBuildCreateView

urlpatterns = patterns('',
    url(r'^$', GroupBuildListView.as_view(), name='groupbuild-list'),
    url(r'^concept/$', GroupBuildCreateView.as_view(), name='create'),
)

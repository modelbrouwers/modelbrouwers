from django.conf.urls import patterns, url

from .views import GroupBuildListView

urlpatterns = patterns('',
    url(r'^$', GroupBuildListView.as_view(), name='groupbuild-list'),
)

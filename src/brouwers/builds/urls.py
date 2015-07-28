from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import (
    BuildAjaxSearchView, BuildDetailView, BuildRedirectView,
    UserBuildListView, index_and_add, BuildUpdate,
    ProfileRedirectView
)


urlpatterns = patterns(
    '',
    # index page, give two possible names
    url(r'^$', index_and_add, name='add_build'),
    url(r'^$', index_and_add, name='index'),

    # backwards compatible, redirect old urls
    url(r'^(?P<build_id>\d+)/$', BuildRedirectView.as_view(), name='old_detail'),
    url(r'^build/(?P<slug>[-_\w]+)/$', BuildDetailView.as_view(), name='detail'),
    url(r'^build/(?P<slug>[-_\w]+)/edit/$', login_required(BuildUpdate.as_view()), name='edit'),

    url(r'^user/(?P<user_id>\d+)/$', UserBuildListView.as_view(), name='user_build_list'),
    url(r'^profile/(?P<profile_id>\d+)/$', ProfileRedirectView.as_view(), name='profile_build_list'),
    )

urlpatterns += patterns(
    '',
    url(r'^search/', BuildAjaxSearchView.as_view(), name='search'),
)

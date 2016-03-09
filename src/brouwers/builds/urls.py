from django.conf.urls import url

from .views import (
    IndexView,
    BuildDetailView, BuildRedirectView,
    UserBuildListView, ProfileRedirectView,
    BuildCreateView, BuildUpdateView,
    ForumUserRedirectView
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^new/$', BuildCreateView.as_view(), name='create'),

    url(r'^(?P<pk>\d+)/$', BuildRedirectView.as_view()),
    url(r'^build/(?P<slug>[-_\w]+)/$', BuildDetailView.as_view(), name='detail'),
    url(r'^build/(?P<slug>[-_\w]+)/edit/$', BuildUpdateView.as_view(), name='update'),

    url(r'^forumuser/(?P<pk>\d+)/$', ForumUserRedirectView.as_view(), name='forum_user_build_list'),
    url(r'^user/(?P<user_id>\d+)/$', UserBuildListView.as_view(), name='user_build_list'),
    url(r'^profile/(?P<profile_id>\d+)/$', ProfileRedirectView.as_view(), name='profile_build_list'),
]

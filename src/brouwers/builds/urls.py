from django.conf.urls import patterns, url

from .views import (
    IndexView,
    BuildDetailView, BuildRedirectView,
    UserBuildListView, ProfileRedirectView,
    # BuildUpdate,
)


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^(?P<pk>\d+)/$', BuildRedirectView.as_view()),
    url(r'^build/(?P<slug>[-_\w]+)/$', BuildDetailView.as_view(), name='detail'),
    # url(r'^build/(?P<slug>[-_\w]+)/edit/$', login_required(BuildUpdate.as_view()), name='edit'),

    url(r'^user/(?P<user_id>\d+)/$', UserBuildListView.as_view(), name='user_build_list'),
    url(r'^profile/(?P<profile_id>\d+)/$', ProfileRedirectView.as_view(), name='profile_build_list'),
    )

# urlpatterns += patterns(
#     '',
#     url(r'^search/', BuildAjaxSearchView.as_view(), name='search'),
# )

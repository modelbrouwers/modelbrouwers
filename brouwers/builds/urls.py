from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required


from general.models import UserProfile


from .models import Build
from .views import BuildDetailView, BuildRedirectView, \
                   UserBuildListView, BuildCreate, BuildUpdate, \
                   ProfileRedirectView


urlpatterns = patterns('',
    # index page
    url(r'^$', BuildCreate.as_view(), name='add_build'),
    
    # backwards compatible, redirect old urls
    url(r'^(?P<build_id>\d+)/$', BuildRedirectView.as_view(), name='old_detail'),
    url(r'^build/(?P<slug>[-_\w]+)/$', BuildDetailView.as_view(), name='detail'),
    url(r'^build/(?P<slug>[-_\w]+)/edit/$', login_required(BuildUpdate.as_view()), name='edit'),
    
    url(r'^user/(?P<user_id>\d+)/$', UserBuildListView.as_view(), name='user_build_list'),
    url(r'^profile/(?P<profile_id>\d+)/$', ProfileRedirectView.as_view(), name='profile_build_list'),
    )
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required


from general.models import UserProfile


from .models import Build
from .views import BuildDetailView, BuildRedirectView, UserBuildListView, BuildCreate


info_profile = {
    'queryset': UserProfile.objects.all(),
    'template_name': 'builds/profile_builds.html',
    'template_object_name': 'profile'
    }

urlpatterns = patterns('builds.views',
    url(r'^$', 'builders_overview'),
    # (r'^add/$', 'add'),
    url(r'^edit/(\d+)/$', 'edit', name='edit'),
    (r'^profile/(?P<object_id>\d+)/$', 'custom_object_detail', info_profile, "profile_detail"),
    )


# CLASS BASED VIEWS
urlpatterns += patterns('',
    url(r'^(?P<build_id>\d+)/$', BuildRedirectView.as_view(), name='old_detail'),
    url(r'^build/(?P<slug>[-_\w]+)/$', BuildDetailView.as_view(), name='detail'),
    # backwards compatible, redirect old urls
    url(r'^(?P<user_id>\d+)/$', UserBuildListView.as_view(), name='user_build_list'),

    url(r'^add/$', login_required(BuildCreate.as_view()), name='add_build'),
    )
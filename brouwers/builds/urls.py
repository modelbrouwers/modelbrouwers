from django.conf.urls.defaults import *
from general.models import UserProfile


from .models import Build
from .views import BuildDetailView


info_profile = {
	'queryset': UserProfile.objects.all(),
	'template_name': 'builds/profile_builds.html',
	'template_object_name': 'profile'
	}

urlpatterns = patterns('builds.views',
	(r'^$', 'builders_overview'),
	(r'^add/$', 'add'),
	url(r'^edit/(\d+)/$', 'edit', name='edit'),
	#(r'^(?P<object_id>\d+)/$', 'custom_object_detail', info_build, "build_detail"),
	(r'^profile/(?P<object_id>\d+)/$', 'custom_object_detail', info_profile, "profile_detail"),
	)


# CLASS BASED VIEWS
urlpatterns += patterns('',
	url(r'^(?P<slug>[-_\w]+)/$',	BuildDetailView.as_view(), name='detail'),
	)
from django.conf.urls.defaults import *
from brouwers.awards.models import UserProfile
from models import Build

info_build = {
	'queryset': Build.objects.all(),
	'template_name': 'builds/build.html',
	'template_object_name': 'build'
	}

info_profile = {
	'queryset': UserProfile.objects.all(),
	'template_name': 'builds/profile_builds.html',
	'template_object_name': 'profile'
	}

urlpatterns = patterns('brouwers.builds.views',
	(r'^$', 'builders_overview'),
	(r'^add/$', 'add'),
	(r'^edit/(\d+)/$', 'edit'),
	(r'^(?P<object_id>\d+)/$', 'custom_object_detail', info_build, "build_detail"),
	(r'^profile/(?P<object_id>\d+)/$', 'custom_object_detail', info_profile, "profile_detail"),
	)

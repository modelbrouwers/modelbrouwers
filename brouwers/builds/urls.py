from django.conf.urls.defaults import *
from brouwers.awards.models import UserProfile
from models import Build

urlpatterns = patterns('brouwers.builds.views',
	(r'^$', 'builders_overview'),
	(r'^add/$', 'add'),
	)

#GENERIC VIEWS

#UserProfile - lists the builds, this one is a detail of a profile
info = {
	'queryset': UserProfile.objects.all(),
	'template_name': 'builds/profile_builds.html',
	'template_object_name': 'profile'
	}

info_build = {
	'queryset': Build.objects.all(),
	'template_name': 'builds/build.html',
	'template_object_name': 'build'
	}

urlpatterns += patterns('django.views.generic.list_detail',
	(r'^(?P<object_id>\d+)/$', 'object_detail', info_build),
	(r'^profile/(?P<object_id>\d+)/$', 'object_detail', info),
	)

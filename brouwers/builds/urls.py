from django.conf.urls.defaults import *
from brouwers.awards.models import UserProfile

urlpatterns = patterns('brouwers.builds.views',
	(r'^$', 'builders_overview'),
	)

#GENERIC VIEWS

#UserProfile - lists the builds, this one is a detail of a profile
info = {
	'queryset': UserProfile.objects.all(),
	'template_name': 'builds/profile_builds.html',
	'template_object_name': 'profile'
	}

urlpatterns += patterns('django.views.generic.list_detail',
	(r'^profile/(?P<object_id>\d+)/$', 'object_detail', info),
	)

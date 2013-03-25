from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/',        include(admin.site.urls)),
    (r'^albums/',       include('albums.urls')),
    (r'^awards/',       include('awards.urls')),
    (r'^forum_tools/',  include('forum_tools.urls')),
    (r'^secret_santa/', include('secret_santa.urls')),
    (r'^shirts/',       include('shirts.urls')),
    (r'^builds/',       include('builds.urls')),
    (r'^ou/',           include('online_users.urls')),
    (r'^migration/',    include('migration.urls')),
    (r'^i18n/',         include('django.conf.urls.i18n')),
    (r'^',              include('general.urls')),
    )

##################
# JS TRANSLATION #
##################
#js_info_dict = {
#    'packages': ('albums',),
#}
#
#urlpatterns += patterns('',
#    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
#)

if settings.DEBUG and settings.DEVELOPMENT:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
		(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
	)

# some sort of catchall, check the database if redirects exist, else return a 404
# this MUST come as last option
urlpatterns += patterns('general.views',
    (r'^([a-z,A-z,/,0-9,-,_]+)/$', 'test_redirects'),
    )

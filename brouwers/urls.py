from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/',        include(admin.site.urls)),
    (r'^albums/',       include('brouwers.albums.urls')),
    (r'^awards/',       include('brouwers.awards.urls')),
    (r'^secret_santa/', include('brouwers.secret_santa.urls')),
    (r'^shirts/',       include('brouwers.shirts.urls')),
    (r'^builds/',       include('brouwers.builds.urls')),
    (r'^ou/',           include('brouwers.online_users.urls')),
    (r'^migration/',    include('brouwers.migration.urls')),
    (r'^i18n/',         include('django.conf.urls.i18n')),
    (r'^',              include('brouwers.general.urls')),
    )

##################
# JS TRANSLATION #
##################
#js_info_dict = {
#    'packages': ('brouwers.albums',),
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
urlpatterns += patterns('brouwers.general.views',
    (r'^([a-z,A-z,/,0-9,-,_]+)/$', 'test_redirects'),
    )

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/',        include(admin.site.urls)),
    url(r'^albums/',       include('albums.urls')),
    url(r'^awards/',       include('awards.urls')),
    url(r'^forum_tools/',  include('forum_tools.urls')),
    url(r'^kitreviews/',   include('kitreviews.urls', namespace='kitreviews')),
    url(r'^secret_santa/', include('secret_santa.urls')),
    url(r'^shirts/',       include('shirts.urls')),
    url(r'^builds/',       include('builds.urls', namespace='builds')),
    url(r'^ou/',           include('online_users.urls')),
    url(r'^migration/',    include('migration.urls')),
    url(r'^i18n/',         include('django.conf.urls.i18n')),
    url(r'^',              include('general.urls')),
)

urlpatterns += staticfiles_urlpatterns()

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

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
		(r'^404/$', TemplateView.as_view(template_name='404.html')),
	)

# some sort of catchall, check the database if redirects exist, else return a 404
# this MUST come as last option
urlpatterns += patterns('general.views',
    (r'^([a-z,A-z,/,0-9,-,_]+(?!\.php$))/$', 'test_redirects'),
    )

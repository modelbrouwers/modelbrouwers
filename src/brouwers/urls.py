import sys

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

admin.autodiscover()

FORUM_URL = settings.PHPBB_URL
if FORUM_URL.startswith('/'):
    FORUM_URL = FORUM_URL[1:]
if not FORUM_URL.endswith('/'):
    FORUM_URL = FORUM_URL+'/'

urlpatterns = patterns('',
    url(r'^admin/rosetta/',include('rosetta.urls')),
    url(r'^admin/',        include(admin.site.urls)),
    url(r'^admin_tools/',  include('admin_tools.urls')),

    url(r'^api/v1/',        include('brouwers.api.urls', namespace='api')),

    url(r'^albums/',       include('brouwers.albums.urls')),
    url(r'^awards/',       include('brouwers.awards.urls')),
    url(r'^brouwersdag/',  include('brouwers.brouwersdag.urls', namespace='brouwersdag')),
    url(r'^forum_tools/',  include('brouwers.forum_tools.urls')),
    url(r'^%s' % FORUM_URL,include('brouwers.forum_tools.urls_phpbb', namespace='phpBB')),
    url(r'^group-builds/', include('brouwers.groupbuilds.urls', namespace='groupbuilds')),
    url(r'^kitreviews/',   include('brouwers.kitreviews.urls', namespace='kitreviews')),
    url(r'^secret_santa/', include('brouwers.secret_santa.urls')),
    url(r'^shirts/',       include('brouwers.shirts.urls')),
    url(r'^builds/',       include('brouwers.builds.urls', namespace='builds')),
    url(r'^ou/',           include('brouwers.online_users.urls')),
    url(r'^migration/',    include('brouwers.migration.urls')),
    url(r'^i18n/',         include('django.conf.urls.i18n')),
    url(r'^',              include('brouwers.users.urls', namespace='users')),
    url(r'^',              include('brouwers.general.urls')),
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
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    )

if 'test' in sys.argv:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

if settings.DEVELOPMENT and not settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

# some sort of catchall, check the database if redirects exist, else return a 404
# this MUST come as last option
urlpatterns += patterns('brouwers.general.views',
    (r'^([a-z,A-z,/,0-9,-,_]+(?!\.php$))/$', 'test_redirects'),
)

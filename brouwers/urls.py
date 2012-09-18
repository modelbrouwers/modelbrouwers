from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^albums/', include('brouwers.albums.urls')),
    (r'^awards/', include('brouwers.awards.urls')),
    (r'^secret_santa/', include('brouwers.secret_santa.urls')),
    (r'^builds/', include('brouwers.builds.urls')),
    (r'^ou/', include('brouwers.online_users.urls')),
    (r'^', include('brouwers.general.urls')),
    )

if settings.DEBUG and settings.DEVELOPMENT:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)


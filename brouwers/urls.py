from django.conf.urls.defaults import *
from brouwers import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^brouwers/', include('brouwers.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('brouwers.general.urls')),
    (r'^awards/', include('brouwers.awards.urls')),
    (r'^secret_santa/', include('brouwers.secret_santa.urls')),
    )

if settings.DEBUG:
	urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)


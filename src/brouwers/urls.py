from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView, RedirectView


# FIXME: this breaks laziness
FORUM_URL = settings.PHPBB_URL
FORUM_URL = FORUM_URL[1:] if FORUM_URL.startswith('/') else FORUM_URL
FORUM_URL = FORUM_URL if FORUM_URL.endswith('/') else FORUM_URL + '/'


urlpatterns = [
    url(r'^admin/rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^api/v1/', include('brouwers.api.urls', namespace='api')),

    # just a placeholder for the url
    url(r'^$', RedirectView.as_view(url='/index.php'), name='index'),

    url(r'^albums/', include('brouwers.albums.urls', namespace='albums')),
    url(r'^awards/', include('brouwers.awards.urls')),
    url(r'^brouwersdag/', RedirectView.as_view(permanent=True, pattern_name='brouwersdag:index')),
    url(r'^forum_tools/', include('brouwers.forum_tools.urls')),
    url(r'^%s' % FORUM_URL, include('brouwers.forum_tools.urls_phpbb', namespace='phpBB')),
    url(r'^group-builds/', include('brouwers.groupbuilds.urls', namespace='groupbuilds')),
    url(r'^kitreviews/', include('brouwers.kitreviews.urls', namespace='kitreviews')),
    url(r'^secret_santa/', include('brouwers.secret_santa.urls', namespace='secret_santa')),
    url(r'^shirts/', TemplateView.as_view(template_name='shirts_removed.html')),
    url(r'^builds/', include('brouwers.builds.urls', namespace='builds')),
    url(r'^ou/', include('brouwers.online_users.urls')),
    url(r'^migration/', include('brouwers.migration.urls')),
    url(r'^modelbouwdag/', include('brouwers.brouwersdag.urls', namespace='brouwersdag')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^', include('brouwers.users.urls', namespace='users')),
    url(r'^', include('brouwers.general.urls')),
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)


if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    ]

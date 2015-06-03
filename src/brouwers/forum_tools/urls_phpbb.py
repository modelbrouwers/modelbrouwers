from django.conf import settings
from django.conf.urls import patterns, url

from django.views.generic import RedirectView


class ForumRedirectView(RedirectView):
    url = settings.PHPBB_URL
    permanent = True


urlpatterns = patterns(
    '',
    url(r'^viewforum.php$',  ForumRedirectView.as_view(), name='viewforum'),
    url(r'^viewtopic.php$',  ForumRedirectView.as_view(), name='viewtopic'),
    url(r'^memberlist.php$',  ForumRedirectView.as_view(), name='memberlist'),
)

from django.conf import settings
from django.conf.urls import url

from django.views.generic import RedirectView


class ForumRedirectView(RedirectView):
    url = settings.PHPBB_URL
    permanent = True


app_name = 'forum_tools'
urlpatterns = [
    url(r'^viewforum.php$', ForumRedirectView.as_view(), name='viewforum'),
    url(r'^viewtopic.php$', ForumRedirectView.as_view(), name='viewtopic'),
    url(r'^memberlist.php$', ForumRedirectView.as_view(), name='memberlist'),
]

from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView


class ForumRedirectView(RedirectView):
    url = settings.PHPBB_URL
    permanent = False


app_name = "forum_tools"
urlpatterns = [
    path("viewforum.php", ForumRedirectView.as_view(), name="viewforum"),
    path("viewtopic.php", ForumRedirectView.as_view(), name="viewtopic"),
    path("memberlist.php", ForumRedirectView.as_view(), name="memberlist"),
]

from django.conf.urls import url

from .views import ForumDetail, TopicDetail

app_name = "forum_tools"

urlpatterns = [
    url(r"^forum/(?P<pk>\d+)/", ForumDetail.as_view(), name="forum-detail"),
    url(r"^topic/(?P<pk>\d+)/", TopicDetail.as_view(), name="topic-detail"),
]

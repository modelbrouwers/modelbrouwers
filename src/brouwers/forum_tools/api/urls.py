from django.urls import path

from .views import ForumDetail, TopicDetail

app_name = "forum_tools"

urlpatterns = [
    path("forum/<int:pk>/", ForumDetail.as_view(), name="forum-detail"),
    path("topic/<int:pk>/", TopicDetail.as_view(), name="topic-detail"),
]

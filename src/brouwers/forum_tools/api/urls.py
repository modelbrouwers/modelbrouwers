from django.conf.urls import url

from .views import ForumDetail, TopicDetail


urlpatterns = [
    url(r'^forum/(?P<pk>\d+)/', ForumDetail.as_view(), name='forum-detail'),
    url(r'^topic/(?P<pk>\d+)/', TopicDetail.as_view(), name='topic-detail'),
]

from django.conf.urls import url

from .viewsets import UserProfileViewSet

urlpatterns = [
    url(r'^profile/$', UserProfileViewSet.as_view(), name='user-profile')
]

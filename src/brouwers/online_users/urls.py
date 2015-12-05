from django.conf.urls import url

from .views import get_online_users, set_online

urlpatterns = [
    url(r'^so/$', set_online),
    url(r'^ous/$', get_online_users),
]

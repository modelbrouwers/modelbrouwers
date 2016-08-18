from django.conf.urls import url

from .views import get_online_users, set_online

app_name = 'online_users'
urlpatterns = [
    url(r'^so/$', set_online),
    url(r'^ous/$', get_online_users),
]

from django.urls import path

from .views import get_online_users, set_online

app_name = "online_users"
urlpatterns = [
    path("so/", set_online),
    path("ous/", get_online_users),
]

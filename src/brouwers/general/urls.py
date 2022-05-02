from django.urls import path

from .ajax_views import AnnouncementView, search_users

app_name = "general"
urlpatterns = [
    path("user/search/", search_users),
    path(
        "utils/get-announcement/", AnnouncementView.as_view(), name="get-announcement"
    ),
]

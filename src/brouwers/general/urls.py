from django.urls import path

from .ajax_views import AnnouncementView

app_name = "general"
urlpatterns = [
    path(
        "utils/get-announcement/", AnnouncementView.as_view(), name="get-announcement"
    ),
]

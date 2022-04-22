from django.urls import path

from .ajax_views import AnnouncementView, search_users
from .views import ServeHbsTemplateView

app_name = "general"
urlpatterns = [
    path(
        "templates/<str:app_name>/<str:template_name>/",
        ServeHbsTemplateView.as_view(),
        name="hbs_template",
    ),
    path("user/search/", search_users),
    path(
        "utils/get-announcement/", AnnouncementView.as_view(), name="get-announcement"
    ),
]

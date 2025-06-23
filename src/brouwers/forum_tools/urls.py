from django.urls import path

from .views import BuildReportForumsView, ModDataView, get_posting_level

# Everything is AJAX
app_name = "forum_tools"
urlpatterns = [
    path("get_post_perm/", get_posting_level),
    path(
        "get_build_report_forums/",
        BuildReportForumsView.as_view(),
        name="get_build_report_forums",
    ),
    path("mods/get_data/", ModDataView.as_view(), name="get_mod_data"),
]

from django.urls import path

from .views import (
    BuildReportForumsView,
    ModDataView,
    SyncDataView,
    get_posting_level,
    get_sharing_perms,
)

# Everything is AJAX
app_name = "forum_tools"
urlpatterns = [
    path("get_sync_data/", SyncDataView.as_view(), name="get_sync_data"),
    path("get_post_perm/", get_posting_level),
    path(
        "get_build_report_forums/",
        BuildReportForumsView.as_view(),
        name="get_build_report_forums",
    ),
    path("mods/get_data/", ModDataView.as_view(), name="get_mod_data"),
    path("mods/get_sharing_perms/", get_sharing_perms, name="get_sharing_perms"),
]

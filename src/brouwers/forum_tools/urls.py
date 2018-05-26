from django.conf.urls import url

from .views import (
    BuildReportForumsView, ChatView, ModDataView, SyncDataView,
    get_posting_level, get_sharing_perms
)

# Everything is AJAX
app_name = 'forum_tools'
urlpatterns = [
    url(r'^get_sync_data/$', SyncDataView.as_view(), name='get_sync_data'),
    url(r'^get_chat/$', ChatView.as_view(), name='get_chat'),
    url(r'^get_post_perm/$', get_posting_level),
    url(r'^get_build_report_forums/$', BuildReportForumsView.as_view(), name='get_build_report_forums'),
    url(r'^mods/get_data/$', ModDataView.as_view(), name='get_mod_data'),
    url(r'^mods/get_sharing_perms/$', get_sharing_perms, name='get_sharing_perms'),
]

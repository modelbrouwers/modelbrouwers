from django.conf.urls import url

from .views import (
    get_sync_data,
    get_chat,
    get_posting_level,
    get_build_report_forums,
    get_mod_data,
    get_sharing_perms,
)

# Everything is AJAX
urlpatterns = [
    url(r'^get_sync_data/$', get_sync_data),
    url(r'^get_chat/$', get_chat),
    url(r'^get_post_perm/$', get_posting_level),
    url(r'^get_build_report_forums/$', get_build_report_forums),
    url(r'^mods/get_data/$', get_mod_data),
    url(r'^mods/get_sharing_perms/$', get_sharing_perms),
]

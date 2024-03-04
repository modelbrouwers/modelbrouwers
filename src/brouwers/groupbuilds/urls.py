from django.urls import path
from django.views.generic import RedirectView

from .views import GroupBuildDetailView, GroupBuildListView

app_name = "groupbuilds"
urlpatterns = [
    path("", GroupBuildListView.as_view(), name="groupbuild-list"),
    path(
        "to-forum/",
        RedirectView.as_view(permanent=False, url="/phpBB3/viewforum.php?f=266"),
        name="to-forum",
    ),
    path("<slug:slug>/", GroupBuildDetailView.as_view(), name="detail"),
]

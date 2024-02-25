from django.urls import path
from django.views.generic import RedirectView

from .views.public import GroupBuildDetailView

app_name = "groupbuilds"
urlpatterns = [
    path(
        "",
        RedirectView.as_view(permanent=False, url="/phpBB3/viewforum.php?f=266"),
        name="groupbuild-list",
    ),
    path("<slug:slug>/", GroupBuildDetailView.as_view(), name="detail"),
]

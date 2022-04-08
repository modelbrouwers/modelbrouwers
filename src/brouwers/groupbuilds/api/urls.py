from django.urls import path

from .views import GroupBuildDetail

app_name = "groupbuilds"

urlpatterns = [
    path("groupbuild/<int:pk>/", GroupBuildDetail.as_view(), name="groupbuild-detail"),
    path(
        "groupbuild/<slug:slug>/",
        GroupBuildDetail.as_view(lookup_field="slug"),
        name="groupbuild-detail",
    ),
]

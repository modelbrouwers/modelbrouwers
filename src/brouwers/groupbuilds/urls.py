from django.urls import path

from .views.admin import (
    GroupBuildCreateView,
    GroupBuildSubmitView,
    GroupBuildUpdateView
)
from .views.participant import (
    GroupBuildParticipateView,
    MyGroupbuildsListView,
    ParticipantUpdateView
)
from .views.public import GroupBuildDetailView, GroupBuildListView

app_name = "groupbuilds"
urlpatterns = [
    path("", GroupBuildListView.as_view(), name="groupbuild-list"),
    path("dashboard/", MyGroupbuildsListView.as_view(), name="dashboard"),
    path("concept/", GroupBuildCreateView.as_view(), name="create"),
    path("<slug:slug>/", GroupBuildDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", GroupBuildUpdateView.as_view(), name="edit"),
    path("<slug:slug>/submit/", GroupBuildSubmitView.as_view(), name="submit"),
    path(
        "<slug:slug>/participate/",
        GroupBuildParticipateView.as_view(),
        name="participate",
    ),
    path(
        "<slug:slug>/participant/<int:pk>/",
        ParticipantUpdateView.as_view(),
        name="update-participant",
    ),
]

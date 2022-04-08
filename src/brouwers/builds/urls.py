from django.urls import path

from .views import (
    BuildCreateView,
    BuildDetailView,
    BuildRedirectView,
    BuildUpdateView,
    ForumUserRedirectView,
    IndexView,
    ProfileRedirectView,
    UserBuildListView
)

app_name = "builds"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new/", BuildCreateView.as_view(), name="create"),
    path("<int:pk>/", BuildRedirectView.as_view()),
    path("build/<slug:slug>/", BuildDetailView.as_view(), name="detail"),
    path("build/<slug:slug>/edit/", BuildUpdateView.as_view(), name="update"),
    path(
        "forumuser/<int:pk>/",
        ForumUserRedirectView.as_view(),
        name="forum_user_build_list",
    ),
    path("user/<int:user_id>/", UserBuildListView.as_view(), name="user_build_list"),
    path(
        "profile/<int:profile_id>/",
        ProfileRedirectView.as_view(),
        name="profile_build_list",
    ),
]

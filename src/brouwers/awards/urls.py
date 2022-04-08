from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
    CategoryListView,
    NominationListView,
    NominationView,
    VoteView,
    WinnersView,
    scores,
    vote_overview
)

# app_name = 'awards'
urlpatterns = [
    path("vote/overview/", vote_overview),
    path("vote/scores/", scores),
    path(
        "", TemplateView.as_view(template_name="awards/base.html"), name="awards_index"
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", NominationListView.as_view()),
    path(
        "categories/<slug:slug>/", NominationListView.as_view(), name="nominations-list"
    ),
    path("nomination/", NominationView.as_view(), name="add_nomination"),
    path("voting/", VoteView.as_view(), name="voting"),
    path("winners/<int:year>/", WinnersView.as_view(), name="winners"),
    path("winners/", WinnersView.as_view(), name="winners"),
]

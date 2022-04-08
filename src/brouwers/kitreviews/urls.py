from django.urls import path

from .views import (
    AddReview,
    IndexView,
    KitReviewDetail,
    KitSearchView,
    LegacyRedirectView,
    ReviewListView
)

app_name = "kitreviews"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("add/", AddReview.as_view(), name="add_review"),
    path("search/", KitSearchView.as_view(), name="find_kit"),
    path("kit/<slug>/reviews/", ReviewListView.as_view(), name="review-list"),
    path(
        "kit/<slug>/reviews/<int:pk>/", KitReviewDetail.as_view(), name="review-detail"
    ),
    path("kit/<slug>/reviews/add/", AddReview.as_view(), name="review-add"),
    # legacy urls
    path("kitreview_search_result_review.php", LegacyRedirectView.as_view()),
]

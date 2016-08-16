from django.conf.urls import url

from .views import (
    AddReview, IndexView, KitReviewDetail, KitSearchView, LegacyRedirectView,
    ReviewListView
)

app_name = 'kitreviews'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add/$', AddReview.as_view(), name='add_review'),
    url(r'^search/$', KitSearchView.as_view(), name='find_kit'),
    url(r'^kit/(?P<slug>[\w-]+)/reviews/$', ReviewListView.as_view(), name='review-list'),
    url(r'^kit/(?P<slug>[\w-]+)/reviews/(?P<pk>\d+)/$', KitReviewDetail.as_view(), name='review-detail'),
    url(r'^kit/(?P<slug>[\w-]+)/reviews/add/$', AddReview.as_view(), name='review-add'),

    # legacy urls
    url(r'^kitreview_search_result_review\.php$', LegacyRedirectView.as_view()),
]

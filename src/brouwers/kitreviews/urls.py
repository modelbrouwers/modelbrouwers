from django.conf.urls import url

from .views import (
    AddReview, KitSearchView, IndexView, KitReviewDetail, ReviewListView
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add/$', AddReview.as_view(), name='add_review'),
    url(r'^search/$', KitSearchView.as_view(), name='find_kit'),
    url(r'^kit/(?P<slug>[\w-]+)/reviews/$', ReviewListView.as_view(), name='review-list'),
    url(r'^kit/(?P<slug>[\w-]+)/reviews/add/$', AddReview.as_view(), name='review-add'),

    url(r'^kit/(?P<pk>\d+)/$', KitReviewDetail.as_view(), name='kit_detail'),
]

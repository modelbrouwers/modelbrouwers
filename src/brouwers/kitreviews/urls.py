from django.conf.urls import url

from .views import (
    AddReview, FindKit, IndexView, KitReviewDetail, ReviewListView
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add/$', AddReview.as_view(), name='add_review'),
    url(r'^find_kit/$', FindKit.as_view(), name='find_kit'),
    url(r'^kit/(?P<slug>[\w-]+)/reviews/$', ReviewListView.as_view(), name='review-list'),

    url(r'^kit/$', KitReviewDetail.as_view()),
    url(r'^kit/(?P<pk>\d+)/$', KitReviewDetail.as_view(), name='kit_detail'),
    url(r'^kit/(?P<pk>\d+)/add_review/$', AddReview.as_view(), name='kit_add_review'),
]

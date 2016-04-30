from django.conf.urls import url

from .views import AddReview, FindKit, IndexView, KitDetail


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add/$', AddReview.as_view(), name='add_review'),
    url(r'^find_kit/$', FindKit.as_view(), name='find_kit'),
    url(r'^kit/$', KitDetail.as_view()),
    url(r'^kit/(\d+)/$', KitDetail.as_view(), name='kit_detail'),
    url(r'^kit/(\d+)/add_review/$', AddReview.as_view(), name='kit_add_review'),
]

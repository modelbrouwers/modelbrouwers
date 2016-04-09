from django.conf.urls import url

from .views import index, AddReview, find_kit, kit_detail


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add/$', AddReview.as_view(), name='add_review'),
    url(r'^find_kit/$', find_kit, name='find_kit'),
    url(r'^kit/$', kit_detail),
    url(r'^kit/(\d+)/$', kit_detail, name='kit_detail'),
    url(r'^kit/(\d+)/add_review/$', AddReview.as_view(), name='kit_add_review'),
]

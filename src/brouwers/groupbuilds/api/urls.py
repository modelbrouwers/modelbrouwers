from django.conf.urls import url

from .views import GroupBuildDetail

urlpatterns = [
    url(r'^groupbuild/(?P<pk>\d+)/$', GroupBuildDetail.as_view(), name='groupbuild-detail'),
    url(r'^groupbuild/(?P<slug>[\w\-_]+)/$', GroupBuildDetail.as_view(lookup_field='slug'), name='groupbuild-detail'),
]

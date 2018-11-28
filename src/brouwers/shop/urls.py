from django.conf.urls import url

from .views import IndexView, CategoryDetailView

app_name = 'shop'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<slug>[-_\w]+)/', CategoryDetailView.as_view(), name='category-detail')
]

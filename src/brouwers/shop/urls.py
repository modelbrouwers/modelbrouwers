from django.conf.urls import url
from django.views.generic import TemplateView

from .views import IndexView, CategoryDetailView

app_name = 'shop'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^categories/(?P<slug>[-_\w]+)/', CategoryDetailView.as_view(), name='category-detail'),
    url(r'^products/(?P<slug>[-_\w]+)/', TemplateView.as_view(template_name='shop/product_detail.html'),
        name='product-detail')
]

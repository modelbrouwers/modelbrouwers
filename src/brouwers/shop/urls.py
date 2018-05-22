from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import IndexView

app_name = 'shop'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<slug>[-_\w]+)/', TemplateView.as_view(template_name='shop/product_list.html'), name='product-list')
]

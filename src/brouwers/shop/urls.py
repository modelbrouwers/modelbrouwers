from django.conf.urls import url

from .debug_views import IdealPaymentView, PaymentView
from .views import (
    CartDetailView, CategoryDetailView, IndexView, ProductDetailView
)

app_name = 'shop'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^categories/(?P<slug>[-_\w]+)/', CategoryDetailView.as_view(), name='category-detail'),
    url(r'^products/(?P<slug>[-_\w]+)/', ProductDetailView.as_view(), name='product-detail'),
    url(r'^cart/(?P<pk>\d+)/', CartDetailView.as_view(), name='cart-detail'),

    url(r'^pay/$', PaymentView.as_view(), name='pay'),
    url(r'^pay/ideal/$', IdealPaymentView.as_view(), name='ideal-bank'),
]

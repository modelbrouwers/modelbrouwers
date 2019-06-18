from django.conf.urls import url

from .viewsets import CartViewSet

urlpatterns = [
    url(r'^cart/$', CartViewSet.as_view(), name='cart-detail'),
]

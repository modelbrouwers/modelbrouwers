from django.conf.urls import url

from .viewsets import CartViewSet, IdealBanksViewSet

urlpatterns = [
    url(r'^cart/$', CartViewSet.as_view(), name='cart-detail'),
    url(r'^ideal_banks/$', IdealBanksViewSet.as_view(), name='ideal-banks')
]

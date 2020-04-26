from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from brouwers.albums.api.views import (
    MyAlbumsViewset, MyPhotosViewset, PhotoViewSet, PreferencesViewSet
)
from brouwers.groupbuilds.api.viewsets import ParticipantViewSet
from brouwers.kits.api.views import (
    BoxartViewSet, BrandViewSet, ModelKitViewSet, ScaleViewSet
)
from brouwers.shop.api.viewsets import (
    CartProductViewSet, PaymentMethodViewSet, ProductViewSet
)

router = DefaultRouter()

# albums
router.register(r'albums/photo', PhotoViewSet)
router.register(r'albums/preferences', PreferencesViewSet)
router.register(r'my/albums', MyAlbumsViewset, basename='my/albums')
router.register(r'my/photos', MyPhotosViewset, basename='my/photos')
router.register(r'kits/kit', ModelKitViewSet)
router.register(r'kits/brand', BrandViewSet)
router.register(r'kits/scale', ScaleViewSet)
router.register(r'kits/boxart', BoxartViewSet)

# groupbuilds
router.register(r'groupbuilds/participant', ParticipantViewSet)

# shop
# router.register(r'shop/cart', CartViewSet)
router.register(r'shop/cart-product', CartProductViewSet)
router.register(r'shop/product', ProductViewSet)
router.register(r'shop/paymentmethod', PaymentMethodViewSet)

app_name = 'api'
urlpatterns = [
    url(r'^builds/', include('brouwers.builds.api.urls', namespace='builds')),
    url(r'^forum_tools/', include('brouwers.forum_tools.api.urls', namespace='forum_tools')),
    url(r'^groupbuilds/', include('brouwers.groupbuilds.api.urls', namespace='groupbuilds')),
    url(r'^shop/', include('brouwers.shop.api.urls')),
] + router.urls

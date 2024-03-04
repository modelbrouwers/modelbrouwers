from django.urls import include, path

from rest_framework.routers import DefaultRouter

from brouwers.albums.api.views import (
    MyAlbumsViewset,
    MyPhotosViewset,
    PhotoViewSet,
    PreferencesViewSet,
)
from brouwers.kits.api.views import (
    BoxartViewSet,
    BrandViewSet,
    ModelKitViewSet,
    ScaleViewSet,
)
from brouwers.shop.api.viewsets import (
    CartProductViewSet,
    PaymentMethodViewSet,
    ProductViewSet,
)

router = DefaultRouter()

# albums
router.register("albums/photo", PhotoViewSet)
router.register("albums/preferences", PreferencesViewSet)
router.register("my/albums", MyAlbumsViewset, basename="my/albums")
router.register("my/photos", MyPhotosViewset, basename="my/photos")
router.register("kits/kit", ModelKitViewSet)
router.register("kits/brand", BrandViewSet)
router.register("kits/scale", ScaleViewSet)
router.register("kits/boxart", BoxartViewSet)

# shop
# router.register(r'shop/cart', CartViewSet)
router.register("shop/cart-product", CartProductViewSet)
router.register("shop/product", ProductViewSet)
router.register("shop/paymentmethod", PaymentMethodViewSet)

app_name = "api"
urlpatterns = [
    path("builds/", include("brouwers.builds.api.urls")),
    path("forum_tools/", include("brouwers.forum_tools.api.urls")),
    path("groupbuilds/", include("brouwers.groupbuilds.api.urls")),
    path("shop/", include("brouwers.shop.api.urls")),
    path("users/", include("brouwers.users.api.urls")),
] + router.urls

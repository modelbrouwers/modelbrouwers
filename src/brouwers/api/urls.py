from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from brouwers.albums.api.views import (
    MyAlbumsViewset, MyPhotosViewset,
    PhotoViewSet, PreferencesViewSet
)
from brouwers.kits.api.views import ModelKitViewSet, BrandViewSet

router = DefaultRouter()

# albums
router.register(r'albums/photo', PhotoViewSet)
router.register(r'albums/preferences', PreferencesViewSet)
router.register(r'my/albums', MyAlbumsViewset, base_name='my/albums')
router.register(r'my/photos', MyPhotosViewset, base_name='my/photos')
router.register(r'kits/kit', ModelKitViewSet)
router.register(r'kits/brand', BrandViewSet)


urlpatterns = router.urls + patterns(
    '',
    url(r'^forum_tools/', include('brouwers.forum_tools.api.urls', namespace='forum_tools')),
    url(r'^groupbuilds/', include('brouwers.groupbuilds.api.urls', namespace='groupbuilds')),
)

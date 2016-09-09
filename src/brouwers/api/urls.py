from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from brouwers.albums.api.views import (
    MyAlbumsViewset, MyPhotosViewset, PhotoViewSet, PreferencesViewSet
)
from brouwers.groupbuilds.api.viewsets import ParticipantViewSet
from brouwers.kits.api.views import BrandViewSet, ModelKitViewSet, ScaleViewSet

router = DefaultRouter()

# albums
router.register(r'albums/photo', PhotoViewSet)
router.register(r'albums/preferences', PreferencesViewSet)
router.register(r'my/albums', MyAlbumsViewset, base_name='my/albums')
router.register(r'my/photos', MyPhotosViewset, base_name='my/photos')
router.register(r'kits/kit', ModelKitViewSet)
router.register(r'kits/brand', BrandViewSet)
router.register(r'kits/scale', ScaleViewSet)

# groupbuilds
router.register(r'groupbuilds/participant', ParticipantViewSet)

app_name = 'api'
urlpatterns = [
    url(r'^builds/', include('brouwers.builds.api.urls', namespace='builds')),
    url(r'^forum_tools/', include('brouwers.forum_tools.api.urls', namespace='forum_tools')),
    url(r'^groupbuilds/', include('brouwers.groupbuilds.api.urls', namespace='groupbuilds')),
] + router.urls

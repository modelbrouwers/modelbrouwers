from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from brouwers.albums.api.views import PhotoViewSet, PreferencesViewSet

router = DefaultRouter()
router.register(r'albums/photo', PhotoViewSet)
router.register(r'albums/preferences', PreferencesViewSet)

urlpatterns = router.urls + patterns(
    '',
    url(r'^forum_tools/', include('brouwers.forum_tools.api.urls', namespace='forum_tools')),
    url(r'^groupbuilds/', include('brouwers.groupbuilds.api.urls', namespace='groupbuilds')),
)

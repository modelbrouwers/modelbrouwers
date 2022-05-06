from django.urls import path

from .views import UserSelfView

urlpatterns = [
    path("me/", UserSelfView.as_view(), name="user-profile"),
]

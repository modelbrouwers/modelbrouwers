from django.urls import path

from .views import EmailWrapperTestView

app_name = "emails"
urlpatterns = [
    path("wrapper/", EmailWrapperTestView.as_view(), name="wrapper"),
]

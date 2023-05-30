from django.urls import path

from brouwers.shop.views import OrderConfirmationEmailView

from .views import EmailWrapperTestView

app_name = "emails"
urlpatterns = [
    path("wrapper/", EmailWrapperTestView.as_view(), name="wrapper"),
    path("order/<int:pk>/", OrderConfirmationEmailView.as_view(), name="shop-order"),
]

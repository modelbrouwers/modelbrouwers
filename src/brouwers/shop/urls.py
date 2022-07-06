from django.urls import path

from .debug_views import IdealPaymentView, PaymentView
from .payments.sisow.views import PaymentCallbackView
from .views import (
    CartDetailView,
    CategoryDetailView,
    CheckoutView,
    ConfirmOrderView,
    IndexView,
    ProductDetailView,
)

app_name = "shop"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # TODO: drop categories/ prefix & trailing slash
    path(
        "categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"
    ),
    # TODO: change to /<category_slug>/<product_slug>
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("cart/<int:pk>/", CartDetailView.as_view(), name="cart-detail"),
    # payments
    path(
        "payment/<int:pk>/callback/",
        PaymentCallbackView.as_view(),
        name="sisow-payment-callback",
    ),
    path("checkout/confirm", ConfirmOrderView.as_view(), name="confirm-checkout"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout/<path:path>", CheckoutView.as_view(), name="checkout"),
    # debug helpers
    path("pay/", PaymentView.as_view(), name="pay"),
    path("pay/ideal/", IdealPaymentView.as_view(), name="ideal-bank"),
]

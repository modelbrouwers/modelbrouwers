from django.urls import include, path

from .payments.paypal.views import (
    CancelView as PPCancelView,
    ReturnView as PPReturnView,
)
from .payments.sisow.views import PaymentCallbackView as SisowCallbackView
from .views import (
    CartDetailView,
    CheckoutView,
    ConfirmOrderView,
    IndexView,
    OrderListView,
    RouterView,
)

app_name = "shop"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "backoffice/",
        include(
            [
                path("orders/", OrderListView.as_view(), name="order-list"),
            ]
        ),
    ),
    path("cart/<int:pk>/", CartDetailView.as_view(), name="cart-detail"),
    # payments
    path(
        "payments/sisow/<int:pk>/callback/",
        SisowCallbackView.as_view(),
        name="sisow-payment-callback",
    ),
    path(
        "payments/paypal/<int:pk>/return", PPReturnView.as_view(), name="paypal-return"
    ),
    path(
        "payments/paypal/<int:pk>/cancel", PPCancelView.as_view(), name="paypal-cancel"
    ),
    # checkout flow
    path("checkout/confirm", ConfirmOrderView.as_view(), name="confirm-checkout"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout/<path:path>", CheckoutView.as_view(), name="checkout"),
    # catch-all for catalogue routing - note that the individual
    # views are registered inside of RouterView
    path("<path:path>", RouterView.as_view(), name="catalogue"),
]

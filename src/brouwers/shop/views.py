import json
from urllib.parse import urlencode

from django.db import transaction
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import ModelFormMixin

from brouwers.users.api.serializers import UserWithProfileSerializer

from .constants import CART_SESSION_KEY, CartStatuses
from .models import (
    Cart,
    Category,
    CategoryCarouselImage,
    HomepageCategory,
    Order,
    Payment,
    Product,
)
from .payments.service import register, start_payment
from .serializers import ConfirmOrderSerializer


class IndexView(ListView):
    queryset = HomepageCategory.objects.select_related("main_category").order_by(
        "order"
    )
    context_object_name = "categories"
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel_images"] = CategoryCarouselImage.objects.filter(visible=True)
        return context


class CategoryDetailView(DetailView):
    context_object_name = "category"
    template_name = "shop/category_detail.html"
    model = Category


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "shop/product_detail.html"


class CartDetailView(DetailView):
    queryset = Cart.objects.all()
    template_name = "shop/cart_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.for_request(self.request)


class CheckoutMixin:
    template_name = "shop/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_profile_data"] = UserWithProfileSerializer(
                instance=self.request.user,
                context={"request": self.request},
            ).data
        else:
            context["user_profile_data"] = {}

        if order_id := self.request.GET.get("orderId"):
            order = get_object_or_404(Order, id=order_id)
            plugin = register[order.payment.payment_method.method]

            context["orderDetails"] = {
                "number": order.reference,
                "message": plugin.get_confirmation_message(order),
            }
        return context


class CheckoutView(CheckoutMixin, TemplateView):
    pass


class ConfirmOrderView(CheckoutMixin, TemplateResponseMixin, ContextMixin, View):
    """
    Submit an order and redirect to the selected payment provider.

    This view finalizes the cart and creates the actual order. On success, the user
    is redirected to the payment provider.
    """

    @transaction.atomic()
    def post(self, request) -> HttpResponseBase:
        raw_data = request.POST.get("checkoutData")
        serializer = ConfirmOrderSerializer(
            data=json.loads(raw_data) if raw_data else None,
            context={"request": request},
        )

        # validation errors - render back to frontend
        if not serializer.is_valid():
            context = self.get_context_data(serializer=serializer)
            return self.render_to_response(context)

        # everything is valid, proceed to checkout
        cart = serializer.validated_data["cart"]
        payment_method = serializer.validated_data["payment_method"]
        bank = serializer.validated_data.get("bank")

        # create a payment instance for the order
        cart.status = CartStatuses.payment_pending
        cart.save_snapshot()
        cart.save()
        # convert euros to eurocents
        total_amount = int(cart.total * 100)
        payment = Payment.objects.create(
            payment_method=payment_method,
            amount=total_amount,
            cart=cart,
            data={"bank": int(bank.id)} if bank else {},  # TODO: handle non-ideal!
        )

        # store order
        order = serializer.save_order(payment=payment)

        # remove cart from session
        if self.request.session.get(CART_SESSION_KEY) == cart.id:
            del self.request.session[CART_SESSION_KEY]

        success_url = self.get_success_url(order)
        start_payment_response = start_payment(
            payment,
            request=self.request,
            next_page=success_url,
            order=order,
        )
        if start_payment_response is not None:
            return start_payment_response
        return redirect(success_url)

    def get_success_url(self, order: Order) -> str:
        """
        Add the frontend URL routing part to the backend URL.
        """
        # TODO: add token of some sorts to prevent enumeration attacks
        query = urlencode({"orderId": order.id})
        backend_url = reverse("shop:checkout")
        return f"{backend_url}confirmation?{query}"

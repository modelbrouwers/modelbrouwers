import json
import logging
import re
from collections.abc import Sequence
from functools import partial
from typing import Callable
from urllib.parse import urlsplit

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404, HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404, redirect
from django.urls import Resolver404, get_resolver, reverse
from django.urls.converters import SlugConverter
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from brouwers.users.api.serializers import UserWithProfileSerializer

from ..constants import (
    CART_SESSION_KEY,
    ORDERS_SESSION_KEY,
    CartStatuses,
    PaymentStatuses,
)
from ..emails import send_order_confirmation_email
from ..models import (
    Cart,
    Category,
    CategoryCarouselImage,
    HomepageCategory,
    Order,
    Payment,
    Product,
)
from ..payments.service import register, start_payment
from ..serializers import ConfirmOrderSerializer
from ..utils import ViewFunc, view_instance
from .mixins import TestPermissionsRequiredMixin

logger = logging.getLogger(__name__)


class IndexView(TestPermissionsRequiredMixin, ListView):
    queryset = HomepageCategory.objects.select_related("main_category").order_by(
        "order"
    )
    context_object_name = "categories"
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel_images"] = CategoryCarouselImage.objects.filter(visible=True)
        return context


def _call_detail_view(
    candidate: Callable[..., HttpResponseBase],
    *,
    request: HttpRequest,
    slug: str,
) -> HttpResponseBase:
    return candidate(request, slug=slug)


class RouterView(TestPermissionsRequiredMixin, View):
    """
    Route the path to the most appropriate specialized view.

    This attempts to get:

    * product detail from the last slug in the path
    * category detail from the last slug in the path
    * TODO: search by manufacturer
    """

    def dispatch(self, request: HttpRequest, path: str):
        slug = self._validate_path(path)
        callback = partial(_call_detail_view, request=request, slug=slug)
        return self.try_candidates(callback)

    @staticmethod
    def _validate_path(path: str) -> str:
        bits = path.split("/")
        re_slug = re.compile(rf"^{SlugConverter.regex}$")
        if not all(re_slug.match(bit) for bit in bits):
            raise Http404("No catalogue resource found.")
        return bits[-1]

    @staticmethod
    def try_candidates[T](callback: Callable[..., T]) -> T:
        candidates: Sequence[Callable[..., HttpResponseBase]] = (
            ProductDetailView.as_view(),
            CategoryDetailView.as_view(),
        )
        for candidate in candidates:
            try:
                return callback(candidate)
            except Http404:
                continue
        raise Http404("No catalogue resource found.")


class CategoryDetailView(TestPermissionsRequiredMixin, DetailView):
    model = Category
    template_name = "shop/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["products"] = self.object.products.filter(active=True)
        return ctx


class ProductDetailView(TestPermissionsRequiredMixin, DetailView):
    queryset = Product.objects.filter(active=True)
    context_object_name = "product"
    template_name = "shop/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = self._resolve_product_category()
        except Category.DoesNotExist:
            category = context["product"].categories.first()
        context["from_category"] = category
        return context

    def _resolve_product_category(self):
        referrer = self.request.headers.get("Referer")
        if not referrer:  # fallback
            raise Category.DoesNotExist("No Referer header to derive category from")

        split_result = urlsplit(referrer)
        if split_result.netloc != self.request.get_host():
            raise Category.DoesNotExist("Referer belongs to another domain")

        resolver = get_resolver()
        try:
            callback, _, callback_kwargs = resolver.resolve(split_result.path)
        except Resolver404 as exc:
            raise Category.DoesNotExist("Could not resolve referer URL") from exc

        if getattr(callback, "view_class", None) is not RouterView:
            raise Category.DoesNotExist("URL did not resolve to category detailview")

        slug = RouterView._validate_path(callback_kwargs["path"])

        def _try_candidate(candidate: ViewFunc) -> Category | Product:
            view = view_instance(candidate, slug=slug)
            # args and kwargs must match the respective CategoryDetailView args and kwargs
            return view.get_object()

        try:
            instance = RouterView.try_candidates(_try_candidate)
            if not isinstance(instance, Category):
                raise Http404
            return instance
        except Http404 as err:
            raise Category.DoesNotExist("Category does not exist") from err


class CartDetailView(TestPermissionsRequiredMixin, DetailView):
    queryset = Cart.objects.all()
    template_name = "shop/cart_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.for_request(self.request)


class CheckoutMixin:
    template_name = "shop/checkout.html"
    request: HttpRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: handle existing order instance when returning here from a cancel-flow

        if self.request.user.is_authenticated:
            context["user_profile_data"] = UserWithProfileSerializer(
                instance=self.request.user,
                context={"request": self.request},
            ).data
        else:
            context["user_profile_data"] = None

        if order_id := self.request.GET.get("orderId"):
            order_ids = self.request.session.get(ORDERS_SESSION_KEY, [])
            try:
                order_ids.index(int(order_id))
            except ValueError as exc:
                raise PermissionDenied("Invalid order ID provided") from exc

            order = get_object_or_404(Order, id=order_id)
            # FIXME: cancelled payments -> this breaks
            plugin = register[order.payment.payment_method.method]

            context["orderDetails"] = {
                "number": order.reference,
                "message": plugin.get_confirmation_message(order),
            }
        return context


class CheckoutView(TestPermissionsRequiredMixin, CheckoutMixin, TemplateView):
    pass


class ConfirmOrderView(
    TestPermissionsRequiredMixin,
    CheckoutMixin,
    TemplateResponseMixin,
    ContextMixin,
    View,
):
    """
    Submit an order and redirect to the selected payment provider.

    This view finalizes the cart and creates the actual order. On success, the user
    is redirected to the payment provider.
    """

    @transaction.atomic()
    def post(self, request) -> HttpResponseBase:
        raw_data = request.POST.get("checkoutData")
        # find existing order - this happens for example when the payment gets cancelled
        # and you are redirected to the payment screen again, so that the payment can
        # be retried.
        serializer_data = json.loads(raw_data) if raw_data else None
        instance = None
        if (
            serializer_data
            and (cart_id := serializer_data.get("cart"))
            and isinstance(cart_id, int)
        ):
            possible_carts = Cart.objects.for_request(request).filter(id=cart_id)
            instance = Order.objects.filter(cart=possible_carts[:1]).first()
        serializer = ConfirmOrderSerializer(
            data=serializer_data, instance=instance, context={"request": request}
        )

        # validation errors - render back to frontend
        if not serializer.is_valid():
            context = self.get_context_data(serializer=serializer)
            return self.render_to_response(context)

        # everything is valid, proceed to checkout
        cart: Cart = serializer.validated_data["cart"]
        payment_method = serializer.validated_data["payment_method"]
        bank = serializer.validated_data.get("bank")

        # create a payment instance for the order
        cart.status = CartStatuses.processing
        cart.save_snapshot()
        cart.save()

        # store order
        order = serializer.save_order()

        # convert euros to eurocents
        total_amount = int((cart.total + order.shipping_costs) * 100)

        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            status=PaymentStatuses.pending,
            amount=total_amount,
            data={"bank": int(bank.id)} if bank else {},  # TODO: handle non-ideal!
        )

        # remove cart from session
        if self.request.session.get(CART_SESSION_KEY) == cart.id:
            del self.request.session[CART_SESSION_KEY]

        base_url = request.build_absolute_uri(reverse("index"))
        transaction.on_commit(lambda: send_order_confirmation_email(order, base_url))

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
        order_ids = self.request.session.get(ORDERS_SESSION_KEY, [])
        order_ids.append(order.pk)
        self.request.session[ORDERS_SESSION_KEY] = order_ids
        return order.get_confirmation_link()

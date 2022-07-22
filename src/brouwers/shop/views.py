import json

from django.db import transaction
from django.http.response import HttpResponseBase, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import ModelFormMixin

from brouwers.shop.payments.sisow.constants import Payments
from brouwers.users.api.serializers import UserWithProfileSerializer

from .constants import CART_SESSION_KEY
from .forms import ProductReviewForm
from .models import (
    Cart,
    Category,
    CategoryCarouselImage,
    HomepageCategory,
    Payment,
    Product,
)
from .payments.sisow.service import start_payment
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


class ProductDetailView(ModelFormMixin, DetailView):
    queryset = Product.objects.annotate_mean_rating()
    context_object_name = "product"
    template_name = "shop/product_detail.html"
    model = Product
    form_class = ProductReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in kwargs:
            context["form"] = self.get_form()
        return context

    def get_success_url(self):
        return reverse("shop:product-detail", kwargs={"slug": self.object.product.slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.reviewer = self.request.user
        form.instance.product = get_object_or_404(Product, slug=self.kwargs["slug"])
        if form.is_valid():
            self.object = form.save()
            return redirect(self.get_success_url())
        self.object = self.get_object()
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)


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
    def post(self, request, *args, **kwargs) -> HttpResponseBase:
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
        cart.save_snapshot()
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

        issuer_url = start_payment(
            payment, request=self.request, next_page=self.get_success_url()
        )
        return HttpResponseRedirect(issuer_url)

    def get_success_url(self) -> str:
        """
        Add the frontend URL routing part to the backend URL.
        """
        backend_url = reverse("shop:checkout")
        return f"{backend_url}confirmation"

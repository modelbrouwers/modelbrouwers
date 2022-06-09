from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.edit import ModelFormMixin

from brouwers.shop.payments.sisow.constants import Payments
from brouwers.users.api.serializers import UserWithProfileSerializer

from .forms import ConfirmOrderForm, ProductReviewForm
from .models import (
    Cart,
    Category,
    CategoryCarouselImage,
    HomepageCategory,
    Payment,
    Product,
)
from .payments.sisow.service import start_ideal_payment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.get_tree().filter(depth=1, enabled=True)
        return context


class ProductDetailView(ModelFormMixin, DetailView):
    queryset = Product.objects.annotate_mean_rating()
    context_object_name = "product"
    template_name = "shop/product_detail.html"
    model = Product
    form_class = ProductReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.get_tree().filter(depth=1, enabled=True)
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


class CheckoutView(TemplateView):
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


class ConfirmOrderView(FormView):
    """
    Submit an order and redirect to the selected payment provider.

    This view finalizes the cart and creates the actual order. On success, the user
    is redirected to the payment provider.
    """

    form_class = ConfirmOrderForm
    template_name = "shop/checkout.html"

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    # TODO: on form invalid, re-render checkout page but put validation errors in
    # json-script for the React component.
    # def form_invalid(self, form):
    #     return super().form_invalid(form)

    @transaction.atomic()
    def form_valid(self, form) -> HttpResponseRedirect:
        cart = form.cleaned_data["cart"]
        payment_method = form.cleaned_data["payment_method"]
        bank = form.cleaned_data.get("bank")

        assert bank is not None, "Currently only ideal payments are supported"

        # create a payment instance for the order
        cart.save_snapshot()
        # convert euros to eurocents
        total_amount = int(cart.total * 100)
        payment = Payment.objects.create(
            payment_method=payment_method,
            amount=total_amount,
            cart=cart,
            data={"bank": int(bank.id)},  # TODO: handle non-ideal!
        )

        # remove cart from session
        if self.request.session.get("cart_id") == cart.id:
            del self.request.session["cart_id"]

        # special case -> get the ideal payment start URL
        if payment_method.method == Payments.ideal:
            issuer_url = start_ideal_payment(
                payment, request=self.request, next_page=self.get_success_url()
            )
            return HttpResponseRedirect(issuer_url)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
        Add the frontend URL routing part to the backend URL.
        """
        backend_url = reverse("shop:checkout")
        return f"{backend_url}confirmation"

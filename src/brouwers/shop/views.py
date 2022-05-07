from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import ModelFormMixin

from brouwers.users.api.serializers import UserWithProfileSerializer

from .forms import ProductReviewForm
from .models import Cart, Category, CategoryCarouselImage, HomepageCategory, Product


class IndexView(ListView):
    queryset = HomepageCategory.objects.all().order_by("order")
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
        return qs.filter(user=self.request.user)


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

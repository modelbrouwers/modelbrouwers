from django.contrib import admin

from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from solo.admin import SingletonModelAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import (
    Address,
    Cart,
    Category,
    CategoryCarouselImage,
    HomepageCategory,
    HomepageCategoryChild,
    Order,
    Payment,
    PaymentMethod,
    Product,
    ProductBrand,
    ProductImage,
    ProductManufacturer,
    ProductReview,
    ShopConfiguration,
)
from .resources import CategoryResource, ProductResource


@admin.register(Category)
class CategoryAdmin(ImportExportMixin, TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ("name", "image", "seo_keyword", "enabled")
    list_filter = ("enabled",)
    search_fields = ("name", "seo_keyword")
    resource_class = CategoryResource
    # TODO - override template to include import-export buttons
    change_list_template = "admin/tree_change_list.html"


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "seo_keyword",
        "brand",
        "model_name",
        "stock",
        "price",
        "vat",
        "description",
        "length",
        "width",
        "height",
        "weight",
        "manufacturer",
        "tag_list",
    )
    list_filter = (
        "brand",
        "categories",
        "manufacturer",
    )
    list_select_related = ("manufacturer",)
    search_fields = (
        "name",
        "seo_keyword",
        "brand__name",
        "model_name",
        "stock",
        "price",
        "length",
        "width",
        "height",
        "weight",
        "manufacturer__name",
    )
    raw_id_fields = ("brand", "related_products", "categories", "manufacturer")
    resource_class = ProductResource

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "reviewer", "text", "rating", "submitted_on")
    list_filter = ("product", "reviewer", "rating", "submitted_on")
    search_fields = ("product", "reviewer", "rating")


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ("name", "logo")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    # list_display = ('product', 'image')
    # list_filter = ('product',)
    search_fields = ("product",)


@admin.register(ProductManufacturer)
class ProductManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(CategoryCarouselImage)
class CategoryCarouselImageAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "visible")
    list_filter = ("title", "image", "visible")
    list_search = ("title", "image", "visible")


@admin.register(HomepageCategory)
class HomepageCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "main_category",
        "order",
    )
    raw_id_fields = ("main_category",)
    list_filter = ("order",)
    list_search = ("order",)


@admin.register(HomepageCategoryChild)
class HomepageCategoryChild(admin.ModelAdmin):
    list_display = ("category", "order")
    raw_id_fields = ("category",)
    list_filter = ("order",)
    list_search = ("order",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "method", "logo", "enabled", "order")
    list_filter = ("enabled",)
    search_fields = ("name", "method")
    ordering = ("order",)


@admin.register(ShopConfiguration)
class ShopConfigurationAdmin(SingletonModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "user",
    )
    list_select_related = ("user",)
    list_filter = ("status",)
    raw_id_fields = ("user",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("reference", "format_amount", "payment_method", "created")
    list_filter = ("created", "payment_method")
    search_fields = ("reference",)
    date_hierarchy = "created"
    ordering = ("-created",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street",
        "number",
        "postal_code",
        "city",
        "country",
        "chamber_of_commerce",
    )
    list_filter = ("country",)
    search_fields = ("street", "postal_code")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("reference", "first_name", "last_name", "email", "status")
    list_select_related = ("cart", "payment")
    search_fields = ("first_name", "last_name", "payment__reference", "email")
    list_filter = ("status",)
    date_hierarchy = "created"
    raw_id_fields = (
        "cart",
        "payment",
        "delivery_address",
        "invoice_address",
    )

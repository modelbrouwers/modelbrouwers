from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportMixin
from modeltranslation.admin import TranslationAdmin
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
    ProductImage,
    ProductManufacturer,
    ShopConfiguration,
)
from .resources import CategoryResource, ProductResource


@admin.register(Category)
class CategoryAdmin(ImportExportMixin, TranslationAdmin, TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ("name", "image", "enabled")
    list_filter = ("enabled",)
    search_fields = ("name", "meta_description")
    resource_class = CategoryResource
    # TODO - override template to include import-export buttons
    change_list_template = "admin/tree_change_list.html"


@admin.register(Product)
class ProductAdmin(ImportExportMixin, TranslationAdmin):
    list_display = (
        "name",
        "model_name",
        "active",
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
        "active",
        "categories",
        "manufacturer",
    )
    list_select_related = ("manufacturer",)
    search_fields = (
        "name",
        "meta_description",
        "model_name",
        "stock",
        "price",
        "length",
        "width",
        "height",
        "weight",
        "manufacturer__name",
    )
    raw_id_fields = ("related_products", "categories", "manufacturer")
    resource_class = ProductResource

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


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
class HomepageCategoryChildAdmin(admin.ModelAdmin):
    list_display = ("category", "order")
    raw_id_fields = ("category",)
    list_filter = ("order",)
    list_search = ("order",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(TranslationAdmin):
    list_display = ("name", "method", "logo", "enabled", "order")
    list_filter = ("enabled",)
    search_fields = ("name", "method")
    ordering = ("order",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        from .payments.service import register

        if db_field.name == "method":
            assert not db_field.choices
            _old = db_field.choices
            db_field.choices = register.get_choices()
            field = super().formfield_for_dbfield(db_field, request, **kwargs)
            db_field.choices = _old
            return field

        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(ShopConfiguration)
class ShopConfigurationAdmin(SingletonModelAdmin, TranslationAdmin):
    fieldsets = (
        (
            _("Sisow/Buckaroo"),
            {
                "fields": (
                    "sisow_test_mode",
                    "sisow_merchant_id",
                    "sisow_merchant_key",
                )
            },
        ),
        (_("Bank transfer"), {"fields": ("bank_transfer_instructions",)}),
    )


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

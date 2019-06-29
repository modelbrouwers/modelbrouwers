# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from solo.admin import SingletonModelAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import (
    Category, CategoryCarouselImage, HomepageCategory, HomepageCategoryChild,
    Payment, PaymentMethod, Product, ProductBrand, ProductImage,
    ProductManufacturer, ProductReview, ShopConfiguration
)
from .resources import CategoryResource, ProductResource


@admin.register(Category)
class CategoryAdmin(ImportExportMixin, TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ('name', 'image', 'seo_keyword', 'enabled')
    list_filter = ('enabled',)
    search_fields = ('name', 'seo_keyword')
    resource_class = CategoryResource
    # TODO - override template to include import-export buttons
    change_list_template = 'admin/tree_change_list.html'


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = (
        'name',
        'seo_keyword',
        'brand',
        'model_name',
        'stock',
        'price',
        'vat',
        'description',
        'length',
        'width',
        'height',
        'weight',
        'manufacturer',
        'tag_list'
    )
    list_filter = (
        'seo_keyword',
        'brand',
        'price',
        'length',
        'width',
        'height',
        'weight',
        'categories',
        'manufacturer',
    )
    list_select_related = ('manufacturer',)
    search_fields = (
        'name',
        'seo_keyword',
        'brand__name',
        'model_name',
        'stock',
        'price',
        'length',
        'width',
        'height',
        'weight',
        'manufacturer__name',
    )
    raw_id_fields = ('brand', 'related_products', 'categories', 'manufacturer')
    resource_class = ProductResource

    def get_queryset(self, request):
        return super(ProductAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'reviewer', 'text', 'rating', 'submitted_on')
    list_filter = ('product', 'reviewer', 'rating', 'submitted_on')
    search_fields = ('product', 'reviewer', 'rating')


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    # list_display = ('product', 'image')
    # list_filter = ('product',)
    search_fields = ('product',)


@admin.register(ProductManufacturer)
class ProductManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(CategoryCarouselImage)
class CategoryCarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'visible')
    list_filter = ('title', 'image', 'visible')
    list_search = ('title', 'image', 'visible')


@admin.register(HomepageCategory)
class HomepageCategoryAdmin(admin.ModelAdmin):
    list_display = ('main_category', 'order',)
    raw_id_fields = ('main_category',)
    list_filter = ('order',)
    list_search = ('order',)


@admin.register(HomepageCategoryChild)
class HomepageCategoryChild(admin.ModelAdmin):
    list_display = ('category', 'order')
    raw_id_fields = ('category',)
    list_filter = ('order',)
    list_search = ('order',)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'method', 'logo', 'enabled', 'order')
    list_filter = ('enabled',)
    search_fields = ('name', 'method')
    ordering = ('order',)


@admin.register(ShopConfiguration)
class ShopConfigurationAdmin(SingletonModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("reference", "format_amount", "payment_method", "created")
    list_filter = ("created", "payment_method")
    search_fields = ("reference",)
    date_hierarchy = "created"
    ordering = ("-created",)

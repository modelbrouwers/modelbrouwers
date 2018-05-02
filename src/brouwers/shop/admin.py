# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (
    Category, Product, ProductBrand, ProductImage, ProductManufacturer,
    ProductReview
)
from .resources import CategoryResource, ProductResource


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'image', 'seo_keyword', 'enabled')
    list_filter = ('name', 'seo_keyword', 'enabled')
    search_fields = ('name', 'seo_keyword')
    resource_class = CategoryResource


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
        'category',
        'manufacturer',
        'tag_list'
    )
    list_filter = (
        'name',
        'seo_keyword',
        'brand',
        'model_name',
        'stock',
        'price',
        'length',
        'width',
        'height',
        'weight',
        'category',
        'manufacturer',
    )
    search_fields = (
        'name',
        'seo_keyword',
        'brand',
        'model_name',
        'stock',
        'price',
        'length',
        'width',
        'height',
        'weight',
        'category',
        'manufacturer',
    )
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
    list_display = ('product', 'image')
    list_filter = ('product',)
    search_fields = ('product',)


@admin.register(ProductManufacturer)
class ProductManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

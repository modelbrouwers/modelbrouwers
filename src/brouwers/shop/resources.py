from __future__ import annotations

from django.utils.functional import cached_property

from autoslug.settings import slugify
from import_export.instance_loaders import CachedInstanceLoader
from import_export.resources import ModelResource

from .models import Category, Product, ProductManufacturer


class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = ("id", "name", "image", "enabled", "meta_description")


class ProductResource(ModelResource):
    class Meta:
        model = Product
        instance_loader_class = CachedInstanceLoader
        use_bulk = True
        fields = (
            "id",
            "name",
            "slug",
            "model_name",
            "stock",
            "price",
            "vat",
            "description",
            "meta_description",
            "length",
            "width",
            "height",
            "weight",
            "manufacturer",
        )

    @cached_property
    def all_manufacturers(self):
        return ProductManufacturer.objects.in_bulk(field_name="id")

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("manufacturer")

    def import_field(self, field, instance, row, is_m2m=False, **kwargs):
        if field.attribute == "manufacturer":
            value = row[field.column_name or field.attribute]
            if value is None:
                return
            try:
                pk = int(value)
            except ValueError:
                return None
            instance.manufacturer = self.all_manufacturers.get(pk)
            return

        super().import_field(field, instance, row, is_m2m=is_m2m, **kwargs)

    def before_save_instance(self, instance: Product, row, **kwargs) -> None:
        if not instance.slug:
            instance.slug = slugify(instance.name)

        if instance.stock is None:
            instance.stock = 0

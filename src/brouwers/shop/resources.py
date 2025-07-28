from __future__ import annotations

from collections import defaultdict
from collections.abc import Collection

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from autoslug.settings import slugify
from import_export import fields
from import_export.instance_loaders import CachedInstanceLoader
from import_export.resources import ModelResource
from import_export.widgets import ManyToManyWidget, Widget
from tablib import Dataset
from taggit.utils import edit_string_for_tags, parse_tags

from .models import Category, Product, ProductManufacturer


class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = ("id", "name", "image", "enabled", "meta_description")


class CategoriesWidget(ManyToManyWidget):

    def render(self, value, obj=None, **kwargs):
        if value is None:
            return ""
        return ",".join(str(cat.pk) for cat in value)


class ProductResource(ModelResource):
    categories = fields.Field(
        attribute="category_ids",
        column_name="categories",
        widget=CategoriesWidget(model=Category),
    )

    _row_to_instance: dict[int, Product]
    _m2m_data: defaultdict[int, dict[str, Collection[int]]]

    class Meta:
        model = Product
        instance_loader_class = CachedInstanceLoader
        use_bulk = True
        chunk_size = 500
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
            "categories",
            "tags",
        )

    # called during export
    def filter_export(
        self, queryset: models.QuerySet[Product], **kwargs
    ) -> models.QuerySet[Product]:
        return queryset.prefetch_related("manufacturer", "categories", "tags")

    def dehydrate_tags(self, instance: Product) -> str:
        return edit_string_for_tags(instance.tags.all())

    # called during import
    def get_queryset(self) -> models.QuerySet[Product]:
        qs = super().get_queryset()
        return qs.prefetch_related(
            "manufacturer",
            models.Prefetch(
                "categories",
                queryset=Category.objects.only("pk"),
                to_attr="category_ids",
            ),
        )

    @cached_property
    def all_manufacturers(self):
        return ProductManufacturer.objects.in_bulk(field_name="id")

    @cached_property
    def all_categories(self):
        return Category.objects.in_bulk(field_name="id")

    def before_import(self, dataset: Dataset, **kwargs) -> None:
        super().before_import(dataset, **kwargs)
        self._row_to_instance = {}
        self._m2m_data = defaultdict(dict)

    def import_instance(
        self, instance: Product, row, *, row_number: int, **kwargs
    ) -> None:
        # modify import hook to validate the categories, since m2m fields are skipped
        # on bulk imports
        try:
            category_ids = [
                int(stripped_x)
                for (x) in row.get("categories", "").split(",")
                if (stripped_x := x.strip())
            ]
        except (ValueError, TypeError) as exc:
            raise ValidationError(
                {
                    "categories": _(
                        "Categories must be a comma separated list of database IDs."
                    )
                }
            )
        else:
            self._m2m_data[row_number]["categories"] = [
                pk for pk in category_ids if pk in self.all_categories
            ]

        super().import_instance(instance, row, **kwargs)

    def import_field(self, field, instance, row, is_m2m=False, **kwargs) -> None:
        match field.column_name:
            case "manufacturer":
                value = row.get(field.column_name or field.attribute)
                if value is None:
                    return
                try:
                    pk = int(value)
                except ValueError:
                    return None
                instance.manufacturer = self.all_manufacturers.get(pk)
            case _:
                super().import_field(field, instance, row, is_m2m=is_m2m, **kwargs)

    def before_save_instance(
        self, instance: Product, row, *, row_number: int, **kwargs
    ) -> None:
        self._row_to_instance[row_number] = instance
        if not instance.slug:
            instance.slug = slugify(instance.name)

        if instance.stock is None:
            instance.stock = 0

    def get_bulk_update_fields(self):
        fields = super().get_bulk_update_fields()
        fields.remove("categories")
        return fields

    def after_import(self, dataset: Dataset, result, **kwargs) -> None:
        # add the product <-> category relations in bulk. ignore_conflicts ensures that
        # duplicates are ignored if the relation already exists (since the m2m field
        # creates a unique constraint).
        # Note that this means we only support *adding* categories via bulk import,
        # removing from categories needs to be done in the UI.
        ProductCategory = Product._meta.get_field("categories").remote_field.through
        product_categories = [
            ProductCategory(product=product, category=self.all_categories[category_id])
            for row_number, product in self._row_to_instance.items()
            for category_id in self._m2m_data[row_number]["categories"]
        ]
        ProductCategory.objects.bulk_create(product_categories, ignore_conflicts=True)

from __future__ import annotations

from collections import defaultdict
from collections.abc import Collection
from typing import TypedDict

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from autoslug.settings import slugify
from import_export import fields
from import_export.instance_loaders import CachedInstanceLoader
from import_export.resources import ModelResource
from import_export.widgets import ManyToManyWidget
from tablib import Dataset
from taggit.models import Tag, TaggedItem
from taggit.utils import edit_string_for_tags, parse_tags

from .models import Category, Product, ProductManufacturer


class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = ("id", "name", "image", "enabled", "meta_description")


class OptimizedM2MWidget(ManyToManyWidget):
    def render(self, value, obj=None, **kwargs):
        if value is None:
            return ""
        return ",".join(str(cat.pk) for cat in value)


class M2MData(TypedDict, total=False):
    categories: Collection[int]
    tags: Collection[str]
    related_products: Collection[int]


class ProductResource(ModelResource):
    categories = fields.Field(
        attribute="category_ids",
        column_name="categories",
        widget=OptimizedM2MWidget(model=Category),
    )
    related_products = fields.Field(
        attribute="related_product_ids",
        column_name="related_products",
        widget=OptimizedM2MWidget(model=Product),
    )

    _row_to_instance: dict[int, Product]
    _m2m_data: defaultdict[int, M2MData]

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
            "related_products",
        )

    # called during export
    def filter_export(
        self, queryset: models.QuerySet[Product], **kwargs
    ) -> models.QuerySet[Product]:
        return queryset.prefetch_related(
            "manufacturer",
            models.Prefetch(
                "categories",
                queryset=Category.objects.only("pk"),
                to_attr="category_ids",
            ),
            models.Prefetch(
                "related_products",
                queryset=Product.objects.only("pk"),
                to_attr="related_product_ids",
            ),
            "tags",
        )

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
            models.Prefetch(
                "related_products",
                queryset=Product.objects.only("pk"),
                to_attr="related_product_ids",
            ),
        )

    @cached_property
    def all_manufacturers(self):
        return ProductManufacturer.objects.in_bulk(field_name="id")

    @cached_property
    def all_categories(self) -> dict[int, Category]:
        return Category.objects.in_bulk(field_name="id")

    @cached_property
    def all_tags(self) -> dict[str, Tag]:
        # return all tags by name - if duplicates exist, the oldest (by PK) is returned
        qs = Tag.objects.only("pk", "name").order_by("pk").distinct().iterator()
        return {tag.name: tag for tag in qs}

    @cached_property
    def all_products(self):
        return Product.objects.in_bulk(field_name="id")

    def before_import(self, dataset: Dataset, **kwargs) -> None:
        super().before_import(dataset, **kwargs)
        self._row_to_instance = {}
        self._m2m_data = defaultdict(M2MData)

    def import_instance(
        self, instance: Product, row, *, row_number: int, **kwargs
    ) -> None:
        # modify import hook to validate the categories, since m2m fields are skipped
        # on bulk imports
        try:
            category_ids = [
                int(stripped_x)
                for (x) in (row.get("categories") or "").split(",")
                if (stripped_x := x.strip())
            ]
        except (ValueError, TypeError) as exc:
            raise ValidationError(
                {
                    "categories": _(
                        "Categories must be a comma separated list of database IDs."
                    )
                }
            ) from exc
        else:
            self._m2m_data[row_number]["categories"] = [
                pk for pk in category_ids if pk in self.all_categories
            ]

        # validate the tags, m2m fields are skipped on bulk imports
        tag_names: Collection[str] = parse_tags(row.get("tags"))
        self._m2m_data[row_number]["tags"] = tag_names

        # validate the related products, since m2m fields are skipped on bulk imports
        try:
            related_product_ids = [
                int(stripped_x)
                for (x) in (row.get("related_products") or "").split(",")
                if (stripped_x := x.strip())
            ]
        except (ValueError, TypeError) as exc:
            raise ValidationError(
                {
                    "related_products": _(
                        "Related products must be a comma separated list of database IDs."
                    )
                }
            ) from exc
        else:
            self._m2m_data[row_number]["related_products"] = [
                pk for pk in related_product_ids if pk in self.all_products
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
        fields.remove("tags")
        fields.remove("related_products")
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
            for category_id in self._m2m_data[row_number].get("categories", ())
        ]
        ProductCategory.objects.bulk_create(product_categories, ignore_conflicts=True)

        # add the tags to product, and create the tags that don't exist yet
        _all_tag_names: set[str] = set()
        for row_m2m_data in self._m2m_data.values():
            _all_tag_names |= set(row_m2m_data.get("tags", ()))

        tags_to_create: Collection[Tag] = []
        for tag_name in _all_tag_names - set(self.all_tags):
            tag = Tag(name=tag_name)
            tag.slug = tag.slugify(tag_name)
            tags_to_create.append(tag)
            self.all_tags[tag_name] = tag
        Tag.objects.bulk_create(tags_to_create, ignore_conflicts=False)
        product_tags = [
            TaggedItem(tag=self.all_tags[tag_name], content_object=product)
            for row_number, product in self._row_to_instance.items()
            for tag_name in self._m2m_data[row_number].get("tags", ())
        ]
        TaggedItem.objects.bulk_create(product_tags, ignore_conflicts=True)

        # add the related product relations in bulk. ignore_conflicts ensures that
        # duplicates are ignored if the relation already exists (since the m2m field
        # creates a unique constraint)
        RelatedProduct = Product._meta.get_field(
            "related_products"
        ).remote_field.through
        related_products = [
            RelatedProduct(
                from_product=product, to_product=self.all_products[product_id]
            )
            for row_number, product in self._row_to_instance.items()
            for product_id in self._m2m_data[row_number].get("related_products", ())
        ]
        RelatedProduct.objects.bulk_create(related_products, ignore_conflicts=True)

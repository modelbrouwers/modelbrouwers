from autoslug.settings import slugify
from import_export.resources import ModelResource

from .models import Category, Product


class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = ("id", "name", "image", "enabled", "meta_description")


class ProductResource(ModelResource):
    class Meta:
        model = Product
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
        )

    def before_save_instance(self, instance: Product, row, **kwargs) -> None:
        if not instance.slug:
            instance.slug = slugify(instance.name)

        if instance.stock is None:
            instance.stock = 0

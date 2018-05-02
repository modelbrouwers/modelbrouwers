from import_export.resources import ModelResource

from .models import Category, Product


class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'seo_keyword', 'enabled')


class ProductResource(ModelResource):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'brand',
            'model_name',
            'stock',
            'price',
            'vat',
            'description',
            'seo_keyword',
            'length',
            'width',
            'height',
            'weight',
            'category',
            'manufacturer'
        )

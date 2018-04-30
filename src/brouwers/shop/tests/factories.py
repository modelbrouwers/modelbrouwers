import factory
import factory.fuzzy

from ..models import Category, Product, ProductBrand, ProductManufacturer


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    seo_keyword = factory.Faker('bs')
    image = factory.django.ImageField()
    path = factory.Faker('bs')
    depth = factory.fuzzy.FuzzyInteger(0, 8)
    numchild = factory.fuzzy.FuzzyInteger(0, 8)

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    model_name = factory.Faker('name')
    stock = factory.fuzzy.FuzzyInteger(1, 8)
    price = factory.fuzzy.FuzzyDecimal(1, 50)
    vat = factory.fuzzy.FuzzyDecimal(0, 25)
    brand = factory.SubFactory(ProductBrand)
    manufacturer = factory.SubFactory(ProductManufacturer)
    category = factory.SubFactory(Category)
    seo_keyword = factory.Faker('bs')

    class Meta:
        model = Product


class ProductBrandFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = ProductBrand


class ProductManufacturerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = ProductManufacturer

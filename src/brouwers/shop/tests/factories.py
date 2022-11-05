import factory
import factory.fuzzy

from brouwers.users.tests.factories import UserFactory

from ..models import (
    Cart,
    CartProduct,
    Category,
    Product,
    ProductBrand,
    ProductManufacturer,
)
from ..payments.registry import register


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "category-{}".format(n))
    seo_keyword = factory.Faker("bs")
    image = factory.django.ImageField()
    path = factory.Faker("bs")
    depth = factory.fuzzy.FuzzyInteger(0, 8)
    numchild = factory.fuzzy.FuzzyInteger(0, 8)

    class Meta:
        model = Category


class ProductBrandFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    logo = factory.django.ImageField(color="blue")

    class Meta:
        model = ProductBrand


class ProductManufacturerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = ProductManufacturer


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    model_name = factory.Faker("name")
    stock = factory.fuzzy.FuzzyInteger(1, 8)
    price = factory.fuzzy.FuzzyDecimal(0, 5)
    vat = factory.fuzzy.FuzzyDecimal(0, 2)
    manufacturer = factory.SubFactory(ProductManufacturerFactory)
    seo_keyword = factory.Faker("bs")

    class Meta:
        model = Product

    class Params:
        with_brand = factory.Trait(
            brand=factory.SubFactory(ProductBrandFactory),
        )

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                if isinstance(category, Category):
                    self.categories.add(category)
                else:
                    self.categories.add(CategoryFactory.create(category=category))


class CartFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Cart


class CartProductFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    cart = factory.SubFactory(CartFactory)
    amount = factory.fuzzy.FuzzyInteger(1, 18)

    class Meta:
        model = CartProduct


class PaymentMethodFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    method = factory.fuzzy.FuzzyChoice((plugin.identifier for plugin in register))

    class Meta:
        model = "shop.PaymentMethod"
        django_get_or_create = ("method",)

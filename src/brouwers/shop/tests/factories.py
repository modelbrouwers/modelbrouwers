import random
import uuid
from decimal import Decimal

import factory
import factory.fuzzy

from brouwers.users.tests.factories import UserFactory

from ..constants import OrderStatuses, PaymentStatuses
from ..models import Cart, CartProduct, Category, Product, ProductManufacturer
from ..payments.registry import register

LOCALES = [
    "nl_NL",
    "nl_BE",
    "fr_BE",
    "en",
    "de_DE",
]


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "category-{}".format(n))

    class Meta:
        model = Category

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # defer creation to treebeard instead of fuzzing the underlying DB fields
        parent = kwargs.pop("parent", None)
        if parent is not None:
            return parent.add_child(**kwargs)
        return model_class.add_root(**kwargs)


class ProductManufacturerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = ProductManufacturer


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    slug = factory.Sequence(lambda n: f"product-{n:04}")
    model_name = factory.Faker("name")
    stock = factory.fuzzy.FuzzyInteger(1, 8)
    price = factory.fuzzy.FuzzyDecimal(0, 5)
    vat = Decimal("0.21")

    class Meta:
        model = Product

    class Params:
        with_image = factory.Trait(image=factory.django.ImageField(width=10, height=10))

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
    class Meta:
        model = Cart

    class Params:
        with_user = factory.Trait(
            user=factory.SubFactory(UserFactory),
        )


class CartProductFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    cart = factory.SubFactory(CartFactory)
    amount = factory.fuzzy.FuzzyInteger(1, 18)

    class Meta:
        model = CartProduct


class AddressFactory(factory.django.DjangoModelFactory):
    street = factory.Faker("street_address", locale=random.choice(LOCALES))
    postal_code = factory.Faker("postcode", locale=random.choice(LOCALES))
    city = factory.Faker("city", locale=random.choice(LOCALES))
    # TODO: properly refactor to django-countries
    country = factory.fuzzy.FuzzyChoice(["N", "B", "D"])

    class Meta:
        model = "shop.Address"


class OrderFactory(factory.django.DjangoModelFactory):
    cart = factory.SubFactory(CartFactory)
    status = OrderStatuses.received
    first_name = factory.Faker("first_name")
    email = factory.Faker("free_email")
    delivery_address = factory.SubFactory(AddressFactory)

    class Meta:
        model = "shop.Order"


class PaymentMethodFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    method = factory.fuzzy.FuzzyChoice((plugin.identifier for plugin in register))

    class Meta:
        model = "shop.PaymentMethod"
        django_get_or_create = ("method",)


class PaymentFactory(factory.django.DjangoModelFactory):
    order = factory.SubFactory(OrderFactory)
    payment_method = factory.SubFactory(PaymentMethodFactory)
    amount = factory.fuzzy.FuzzyInteger(1, 50000)

    class Meta:
        model = "shop.Payment"

    class Params:
        is_cancelled = factory.Trait(
            order=None,
            historical_order=factory.SubFactory(OrderFactory),
            status=PaymentStatuses.cancelled,
        )
        is_paypal = factory.Trait(
            payment_method=factory.SubFactory(
                PaymentMethodFactory, method="paypal_standard"
            ),
            data={
                "paypal_request_id": str(uuid.uuid4()),
                "paypal_order": {"id": "5O190127TN364715T"},
            },
        )

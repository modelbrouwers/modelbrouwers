import random
import uuid
from decimal import Decimal

import factory
import factory.fuzzy

from brouwers.users.tests.factories import UserFactory

from ..constants import DeliveryMethods, OrderStatuses, PaymentStatuses
from ..models import (
    Address,
    Cart,
    CartProduct,
    Category,
    Order,
    Payment,
    PaymentMethod,
    Product,
    ProductManufacturer,
    ShippingCost,
)
from ..payments.registry import register

LOCALES = [
    "nl_NL",
    "nl_BE",
    "fr",
    "en",
    "de_DE",
]


class CategoryFactory(factory.django.DjangoModelFactory[Category]):
    # left-pad to get lexical sort to behave correctly, otherwise the tree insertion
    # is messed up
    name = factory.Sequence(lambda n: f"category-{n:0>4}")

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Category

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # defer creation to treebeard instead of fuzzing the underlying DB fields
        parent = kwargs.pop("parent", None)
        if parent is not None:
            return parent.add_child(**kwargs)
        return model_class.add_root(**kwargs)


class ProductManufacturerFactory(
    factory.django.DjangoModelFactory[ProductManufacturer]
):
    name = factory.Faker("name")

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = ProductManufacturer


class ProductFactory(factory.django.DjangoModelFactory[Product]):
    name = factory.Faker("name")
    slug = factory.Sequence(lambda n: f"product-{n:04}")
    model_name = factory.Faker("name")
    stock = factory.fuzzy.FuzzyInteger(1, 8)
    price = factory.fuzzy.FuzzyDecimal(0, 5)
    vat = Decimal("0.21")

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Product
        skip_postgeneration_save = True

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


class CartFactory(factory.django.DjangoModelFactory[Cart]):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Cart

    class Params:
        with_user = factory.Trait(
            user=factory.SubFactory(UserFactory),
        )


class CartProductFactory(factory.django.DjangoModelFactory[CartProduct]):
    product = factory.SubFactory(ProductFactory)
    cart = factory.SubFactory(CartFactory)
    amount = factory.fuzzy.FuzzyInteger(1, 18)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = CartProduct


class AddressFactory(factory.django.DjangoModelFactory[Address]):
    street = factory.Faker("street_address", locale=random.choice(LOCALES))
    postal_code = factory.Faker("postcode", locale=random.choice(LOCALES))
    city = factory.Faker("city", locale=random.choice(LOCALES))
    # TODO: properly refactor to django-countries
    country = factory.fuzzy.FuzzyChoice(["N", "B", "D"])

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Address


class OrderFactory(factory.django.DjangoModelFactory[Order]):
    cart = factory.SubFactory(CartFactory)
    status = OrderStatuses.received
    first_name = factory.Faker("first_name")
    email = factory.Faker("free_email")
    delivery_method = factory.fuzzy.FuzzyChoice(list(DeliveryMethods.values))
    delivery_address = factory.Maybe(
        "needs_address",
        yes_declaration=factory.SubFactory(AddressFactory),
        no_declaration=None,
    )

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Order

    class Params:
        needs_address = factory.LazyAttribute(
            lambda o: o.delivery_method == DeliveryMethods.mail
        )
        with_payment = factory.Trait(
            payment=factory.RelatedFactory(
                "brouwers.shop.tests.factories.PaymentFactory",
                factory_related_name="order",
            ),
        )


class PaymentMethodFactory(factory.django.DjangoModelFactory[PaymentMethod]):
    name = factory.Faker("word")
    method = factory.fuzzy.FuzzyChoice(plugin.identifier for plugin in register)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = PaymentMethod
        django_get_or_create = ("method",)


class PaymentFactory(factory.django.DjangoModelFactory[Payment]):
    order = factory.SubFactory(OrderFactory)
    payment_method = factory.SubFactory(PaymentMethodFactory)
    amount = factory.fuzzy.FuzzyInteger(1, 50000)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Payment

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
        is_mistercash = factory.Trait(
            payment_method=factory.SubFactory(
                PaymentMethodFactory, method="sisow_mistercash"
            ),
            data={
                "sisow_method": "mistercash",
                "sisow_transaction_request": {
                    "trxid": "TEST080536811624",
                },
            },
        )


class ShippingCostFactory(factory.django.DjangoModelFactory[ShippingCost]):
    # TODO: properly refactor to django-countries
    country = factory.fuzzy.FuzzyChoice(["N", "B", "D"])
    label = factory.fuzzy.FuzzyChoice(["enveloppe", "small package", "large package"])
    max_weight = factory.fuzzy.FuzzyInteger(10, 15_000)
    price = factory.fuzzy.FuzzyDecimal(2.95, 25)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = ShippingCost
        django_get_or_create = ("country", "max_weight")

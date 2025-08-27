"""
Non-API serializers
"""

from decimal import Decimal
from typing import assert_never

from django.db.models import Prefetch
from django.utils.translation import get_language, gettext, gettext_lazy as _

from rest_framework import serializers

from .api.viewsets import PaymentMethodViewSet
from .constants import DeliveryMethods, OrderStatuses
from .models import Address, Cart, CartProduct, Order, ShippingCost
from .payments.payment_options import SisowIDeal
from .payments.service import register
from .payments.sisow.service import get_ideal_banks


class AddressSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Address
        fields = (
            "street",
            "number",
            "postal_code",
            "city",
            "country",
            "company",
            "chamber_of_commerce",
        )


class ConfirmOrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethodViewSet.queryset,
        required=True,
    )
    payment_method_options = serializers.JSONField(allow_null=True)

    delivery_address = AddressSerializer(required=True, allow_null=True)
    invoice_address = AddressSerializer(required=False, allow_null=True)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Order
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "delivery_method",
            "delivery_address",
            "invoice_address",
            "cart",
            "payment_method",
            "payment_method_options",
        )
        extra_kwargs = {
            "cart": {"queryset": Cart.objects.none()},
        }

    def get_fields(self):
        fields = super().get_fields()

        request = self.context["request"]
        cart_field = fields["cart"]
        assert isinstance(cart_field, serializers.PrimaryKeyRelatedField)
        cart_field.queryset = Cart.objects.for_request(request).prefetch_related(
            Prefetch("products", queryset=CartProduct.objects.select_related("product"))
        )

        return fields

    def validate(self, attrs: dict):
        attrs = super().validate(attrs)

        if not attrs["cart"].products.all():
            raise serializers.ValidationError(
                {
                    "cart": serializers.ErrorDetail(
                        gettext(
                            "Checking a cart without any products is not possible."
                        ),
                        code="cart-empty",
                    )
                }
            )

        if (
            attrs["delivery_method"] == DeliveryMethods.mail
            and not attrs["delivery_address"]
        ):
            raise serializers.ValidationError(
                {
                    "delivery_address": _("A delivery address is required."),
                }
            )

        payment_method = attrs["payment_method"]
        options = attrs.get("payment_method_options") or {}

        # TODO: move validation to plugin?

        # check that a bank was selected
        plugin = register[payment_method.method]
        if isinstance(plugin, SisowIDeal):
            bank_id = options.get("bank")
            if not bank_id:
                raise serializers.ValidationError(
                    {
                        "payment_method_options": serializers.ErrorDetail(
                            gettext("Please select your iDeal bank."), code="required"
                        )
                    }
                )
            # check if it's a valid ID
            ideal_banks = get_ideal_banks()
            bank = next(
                (ideal_bank for ideal_bank in ideal_banks if ideal_bank.id == bank_id),
                None,
            )
            if bank is None:
                raise serializers.ValidationError(
                    {
                        "payment_method_options": serializers.ErrorDetail(
                            gettext("Please select a valid bank."), code="invalid"
                        ),
                    }
                )

            # all good - store the bank reference in the cleaned_data
            attrs["bank"] = bank

        return attrs

    def save_order(self):
        """
        Persist the data in an Order instance.
        """
        cart = self.validated_data["cart"]

        match delivery_method := self.validated_data["delivery_method"]:
            case DeliveryMethods.mail:
                delivery_address = Address.objects.create(
                    **self.validated_data["delivery_address"]
                )
                invoice_address_data = self.validated_data.get("invoice_address")
                invoice_address = (
                    Address.objects.create(**invoice_address_data)
                    if invoice_address_data
                    else None
                )
                shipping_costs = ShippingCost.objects.get_price(
                    country=delivery_address.country, weight=cart.weight
                )
            case DeliveryMethods.pickup:
                delivery_address = None
                invoice_address = None
                shipping_costs = Decimal(0)
            case _:  # pragma: no cover
                assert_never(delivery_method)

        # calculate and snapshot shipping costs

        order, _ = Order.objects.update_or_create(
            cart=cart,
            defaults={
                "status": OrderStatuses.received,
                "first_name": self.validated_data["first_name"],
                "last_name": self.validated_data["last_name"],
                "email": self.validated_data["email"],
                "phone": self.validated_data["phone"],
                "delivery_method": self.validated_data["delivery_method"],
                "delivery_address": delivery_address,
                "invoice_address": invoice_address,
                "language": get_language(),
                "shipping_costs": shipping_costs,
            },
        )
        if self.instance:
            assert self.instance == order
        return order

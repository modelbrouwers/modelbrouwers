"""
Non-API serializers
"""
from django.db import transaction
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .api.viewsets import PaymentMethodViewSet
from .constants import OrderStatuses
from .models import Address, Cart, CartProduct, Order, Payment
from .payments.sisow.constants import Payments
from .payments.sisow.service import get_ideal_banks


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
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

    delivery_address = AddressSerializer(required=True)
    invoice_address = AddressSerializer(required=False, allow_null=True)

    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "delivery_address",
            "invoice_address",
            "cart",
            "payment_method",
            "payment_method_options",
        )
        extra_kwargs = {
            "cart": {"queryset": Cart.objects.none()},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context["request"]
        self.fields["cart"].queryset = Cart.objects.for_request(
            request
        ).prefetch_related(
            Prefetch("products", queryset=CartProduct.objects.select_related("product"))
        )

    def validate(self, attrs: dict):
        attrs = super().validate(attrs)

        payment_method = attrs["payment_method"]
        options = attrs.get("payment_method_options") or {}

        # check that a bank was selected
        if payment_method.method == Payments.ideal:
            bank_id = options.get("bank", {}).get("value")
            if not bank_id:
                raise serializers.ValidationError(
                    {
                        "payment_method_options": serializers.ErrorDetail(
                            _("Please select your iDeal bank."), code="required"
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
                            _("Please select a valid bank."), code="invalid"
                        ),
                    }
                )

            # all good - store the bank reference in the cleaned_data
            attrs["bank"] = bank

        return attrs

    @transaction.atomic
    def save_order(self, *, payment: Payment):
        """
        Persist the data in an Order instance.
        """
        delivery_address = Address.objects.create(
            **self.validated_data["delivery_address"]
        )
        invoice_address_data = self.validated_data["invoice_address"]
        invoice_address = (
            Address.objects.create(**invoice_address_data)
            if invoice_address_data
            else None
        )
        order = Order.objects.create(
            cart=self.validated_data["cart"],
            payment=payment,
            status=OrderStatuses.received,
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            email=self.validated_data["email"],
            phone=self.validated_data["phone"],
            delivery_address=delivery_address,
            invoice_address=invoice_address,
        )
        return order

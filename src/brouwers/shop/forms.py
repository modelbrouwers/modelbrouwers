from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _

from brouwers.shop.constants import OrderStatuses
from brouwers.shop.models import MAX_RATING, MIN_RATING, ProductReview
from brouwers.utils.widgets import StarRatingSelect

from .api.viewsets import PaymentMethodViewSet
from .models import Address, Cart, CartProduct, Order, Payment
from .payments.sisow.constants import Payments
from .payments.sisow.service import get_ideal_banks


class ProductReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(n, n) for n in range(MIN_RATING, MAX_RATING + 1)],
        widget=StarRatingSelect(),
    )

    class Meta:
        model = ProductReview
        fields = ["rating", "text"]


class AddressForm(forms.ModelForm):
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


class ConfirmOrderForm(forms.Form):
    cart = forms.ModelChoiceField(
        queryset=Cart.objects.none(),
        required=True,
    )
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethodViewSet.queryset,
        required=True,
    )
    payment_method_options = forms.JSONField()

    first_name = forms.CharField(label=_("first name"), max_length=255)
    last_name = forms.CharField(label=_("last name"), max_length=255, required=False)
    email = forms.EmailField(label=_("email"))
    phone = forms.CharField(label=_("phone number"), max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["cart"].queryset = Cart.objects.for_request(
            request
        ).prefetch_related(
            Prefetch("products", queryset=CartProduct.objects.select_related("product"))
        )

        # add the nested sub-forms
        self.delivery_form = AddressForm(prefix="delivery", data=self.data)
        self.invoice_form = AddressForm(
            prefix="invoice",
            data=self.data,
            empty_permitted=True,
            use_required_attribute=False,
        )

    def is_valid(self) -> bool:
        subforms_valid = all(
            (self.delivery_form.is_valid(), self.invoice_form.is_valid())
        )
        self_valid = super().is_valid()
        return subforms_valid and self_valid

    def clean(self):
        super().clean()
        payment_method = self.cleaned_data.get("payment_method")
        options = self.cleaned_data.get("payment_method_options")

        # check that a bank was selected
        if payment_method.method == Payments.ideal:
            bank_id = options.get("bank", {}).get("value")
            if not bank_id:
                self.add_error(
                    "payment_method_options",
                    ValidationError(
                        _("Please select your iDeal bank."), code="required"
                    ),
                )
            # check if it's a valid ID
            ideal_banks = get_ideal_banks()
            bank = next(
                (ideal_bank for ideal_bank in ideal_banks if ideal_bank.id == bank_id),
                None,
            )
            if bank is None:
                self.add_error(
                    "payment_method_options",
                    ValidationError(_("Please select a valid bank."), code="invalid"),
                )

            # all good - store the bank reference in the cleaned_data
            self.cleaned_data["bank"] = bank

        return self.cleaned_data

    def get_validation_errors(self) -> dict:
        # collect all the validation errors in a format suitable for json-script
        return {
            "payment": self.errors.get_json_data(),
            self.delivery_form.prefix: self.delivery_form.errors.get_json_data(),
            self.invoice_form.prefix: self.invoice_form.errors.get_json_data(),
        }

    @transaction.atomic
    def save_order(self, *, payment: Payment):
        """
        Persist the data in an Order instance.
        """
        delivery_address = self.delivery_form.save()
        invoice_address = (
            self.invoice_form.save() if self.invoice_form.has_changed() else None
        )
        order = Order.objects.create(
            cart=self.cleaned_data["cart"],
            payment=payment,
            status=OrderStatuses.received,
            first_name=self.clenaed_data["first_name"],
            last_name=self.clenaed_data["last_name"],
            email=self.clenaed_data["email"],
            phone=self.clenaed_data["phone"],
            delivery_address=delivery_address,
            invoice_address=invoice_address,
        )
        return order

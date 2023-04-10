from typing import cast

from django import forms
from django.utils.translation import gettext_lazy as _

from ...models import Payment, ShopConfiguration
from .api import calculate_sha1
from .constants import TransactionStatuses
from .service import get_ideal_banks


def coerce_bank(value: str):
    """
    Translate a form field value back to a :class:`Bank` object.
    """
    bank_mapping = {bank.id: bank for bank in get_ideal_banks()}
    return bank_mapping[value]


class CallbackForm(forms.Form):
    """
    Form definition to handle callbacks/redirects from Sisow.

    Sisow redirects the customer back via a GET request to the shop,
    including a bunch of URL parameters. A number of these parameters are
    relevant in protecting against tampering, since anyone can hit these
    URLs.
    """

    trxid = forms.CharField(label=_("transaction id"))
    ec = forms.CharField(label=_("entrance code"), required=True)
    status = forms.ChoiceField(label=_("status"), choices=TransactionStatuses.choices)
    sha1 = forms.CharField(label=_("sha1 transaction"))
    notify = forms.BooleanField(label=_("notify or not?"), required=False)
    callback = forms.BooleanField(label=_("callback or not?"), required=False)

    def __init__(self, payment: Payment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.payment = payment

    def clean_trxid(self) -> str:
        trxid = self.cleaned_data["trxid"]
        sisow_trx = self.payment.data.get("sisow_transaction_request")
        if not sisow_trx:
            raise forms.ValidationError(_("No Sisow transaction data found"))

        if sisow_trx["trxid"] != trxid:
            raise forms.ValidationError(_("Invalid transaction ID"))

        return trxid

    def clean_ec(self) -> str:
        ec = self.cleaned_data["ec"]
        # ec = entrancecode - if empty, this uses the purchase ID, which is equal to
        # our payment reference
        if ec != self.payment.reference:
            raise forms.ValidationError(_("Invalid entrancecode"))
        return ec

    def clean(self) -> None:
        config = cast(ShopConfiguration, ShopConfiguration.get_solo())

        sha1 = self.cleaned_data.get("sha1") or ""
        trxid = self.cleaned_data.get("trxid") or ""
        ec = self.cleaned_data.get("ec") or ""
        status = self.cleaned_data.get("status") or ""

        if all((sha1, trxid, ec, status)):
            expected_sha1 = calculate_sha1(
                trxid, ec, status, config.sisow_merchant_id, config.sisow_merchant_key
            )
            if sha1 != expected_sha1:
                self.add_error("sha1", _("Invalid SHA1"))

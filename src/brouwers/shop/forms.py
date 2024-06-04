from django import forms
from django.utils.translation import gettext_lazy as _

from .constants import OrderStatuses, PaymentStatuses
from .models import Order


class OrderDetailForm(forms.ModelForm):
    payment_status = forms.ChoiceField(
        required=False,
        label=_("Change payment status"),
        choices=PaymentStatuses.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    send_email_notification = forms.BooleanField(
        required=False,
        label=_("Send email notification"),
        initial=True,
    )

    instance: Order | None

    class Meta:
        model = Order
        fields = ("status",)
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.instance

        self.fields["payment_status"].initial = self.instance.payment.status
        # remove blank/empty option
        self.fields["status"].choices = OrderStatuses.choices

    def save(self, *args, **kwargs):
        obj: Order = super().save(*args, **kwargs)
        if (
            new_payment_status := self.cleaned_data.get("payment_status")
        ) != obj.payment.status:
            obj.payment.status = new_payment_status
            obj.payment.save()
        return obj

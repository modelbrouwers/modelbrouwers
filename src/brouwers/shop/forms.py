from django import forms
from django.utils.translation import gettext_lazy as _

from .constants import OrderStatuses
from .models import Order


class OrderDetailForm(forms.ModelForm):
    send_email_notification = forms.BooleanField(
        required=False,
        label=_("Send email notification"),
        initial=True,
    )

    class Meta:
        model = Order
        fields = ("status",)
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove blank/empty option
        self.fields["status"].choices = OrderStatuses.choices

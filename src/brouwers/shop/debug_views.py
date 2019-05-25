from django import forms
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .models import PaymentMethod


class PaymentForm(forms.Form):
    method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.filter(enabled=True),
        label=_("Payment method")
    )

    amount = forms.DecimalField(label=_("amount"))


class PaymentView(FormView):
    form_class = PaymentForm
    template_name = "shop/pay.html"

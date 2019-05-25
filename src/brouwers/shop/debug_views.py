import decimal

from django import forms
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .models import PaymentMethod
from .payments.sisow import (
    Payments, coerce_bank, get_ideal_bank_choices, get_ideal_banks,
    start_ideal_payment
)


class PaymentForm(forms.Form):
    method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.filter(enabled=True),
        label=_("Payment method")
    )

    amount = forms.DecimalField(label=_("amount"))


class iDealForm(forms.Form):
    bank = forms.TypedChoiceField(
        label=_("bank"),
        choices=get_ideal_bank_choices,
        coerce=coerce_bank
    )


class PaymentView(FormView):
    form_class = PaymentForm
    template_name = "shop/pay.html"

    def form_valid(self, form):
        method = form.cleaned_data['method'].method

        self.request.session['amount'] = str(form.cleaned_data['amount'])

        if method == Payments.ideal:
            return redirect('shop:ideal-bank')
        else:
            raise NotImplementedError


class IdealPaymentView(FormView):
    form_class = iDealForm
    template_name = "shop/pay_ideal.html"

    def form_valid(self, form):
        amount = decimal.Decimal(self.request.session['amount'])
        issuer_url = start_ideal_payment(amount, form.cleaned_data['bank'])
        return redirect(issuer_url)

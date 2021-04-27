from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .models import Payment, PaymentMethod
from .payments.sisow.constants import Payments
from .payments.sisow.forms import coerce_bank
from .payments.sisow.service import get_ideal_bank_choices, start_ideal_payment


class PaymentForm(forms.Form):
    method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.filter(enabled=True), label=_("Payment method")
    )

    amount = forms.DecimalField(label=_("amount"))


class iDealForm(forms.Form):
    bank = forms.TypedChoiceField(
        label=_("bank"), choices=get_ideal_bank_choices, coerce=coerce_bank
    )


class PaymentView(FormView):
    form_class = PaymentForm
    template_name = "shop/pay.html"

    def form_valid(self, form):
        payment_method = form.cleaned_data["method"]

        payment = Payment.objects.create(
            payment_method=payment_method,
            amount=100 * form.cleaned_data["amount"],  # euro to euro cents
        )

        self.request.session["payment"] = payment.pk

        if payment_method.method == Payments.ideal:
            return redirect("shop:ideal-bank")
        else:
            raise NotImplementedError


class IdealPaymentView(FormView):
    form_class = iDealForm
    template_name = "shop/pay_ideal.html"

    def form_valid(self, form):
        payment = get_object_or_404(Payment, pk=self.request.session.get("payment"))
        payment.data["bank"] = int(form.cleaned_data["bank"].id)
        payment.save()
        issuer_url = start_ideal_payment(payment, request=self.request)
        return redirect(issuer_url)

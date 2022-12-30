from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .models import Payment, PaymentMethod
from .payments.payment_options import SisowIDeal
from .payments.service import register, start_payment
from .payments.sisow.forms import coerce_bank
from .payments.sisow.service import get_ideal_bank_choices


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
            amount=int(100 * form.cleaned_data["amount"]),  # euro to euro cents
        )

        self.request.session["payment"] = payment.pk

        plugin = register[payment_method.method]
        if isinstance(plugin, SisowIDeal):
            return redirect("shop:ideal-bank")

        response = start_payment(
            payment,
            request=self.request,
            next_page=reverse("shop:pay"),
            order=None,
        )
        if response is not None:
            return response
        raise NotImplementedError("None response not implemented yet")


class IdealPaymentView(FormView):
    form_class = iDealForm
    template_name = "shop/pay_ideal.html"

    def form_valid(self, form):
        payment = get_object_or_404(Payment, pk=self.request.session.get("payment"))
        payment.data["bank"] = int(form.cleaned_data["bank"].id)
        payment.save()
        return start_payment(
            payment,
            request=self.request,
            next_page="",
            order=None,
        )

import decimal

from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.views.generic.edit import BaseFormView

from .models import PaymentMethod
from .payments.sisow import (
    CallbackForm, Payments, coerce_bank, get_ideal_bank_choices,
    get_ideal_banks, start_ideal_payment
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
        issuer_url = start_ideal_payment(amount, form.cleaned_data['bank'], request=self.request)
        return redirect(issuer_url)


class PaymentCallbackView(BaseFormView):
    """
    Payment callback view from Sisow is requested via GET.

    CSRF is not relevant, since we get a sha1 parameter to validate
    authenticity. We do need to massage the BaseFormView into taking the
    GET data instead of POST though.
    """
    form_class = CallbackForm

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.setdefault("data", self.request.GET)
        return kwargs

    def form_invalid(self, form):
        return HttpResponse(
            form.errors.as_json(),
            content_type="application/json",
            status=400,
        )

    def form_valid(self, form):
        import bpdb; bpdb.set_trace()
        return super().form_valid(form)

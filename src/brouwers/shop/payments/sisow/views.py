from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import BaseFormView

from ...models import Payment
from ..utils import get_next_page
from .constants import TransactionStatuses
from .forms import CallbackForm


class PaymentCallbackView(BaseFormView):
    """
    Payment callback view from Sisow is requested via GET.

    CSRF is not relevant, since we get a sha1 parameter to validate
    authenticity. We do need to massage the BaseFormView into taking the
    GET data instead of POST though.
    """

    form_class = CallbackForm
    success_url = reverse_lazy("shop:pay")

    def get(self, request, pk, *args, **kwargs):
        self.payment = get_object_or_404(Payment, pk=pk)
        return self.post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.setdefault("data", self.request.GET)
        kwargs["payment"] = self.payment
        return kwargs

    def form_invalid(self, form):
        return HttpResponse(
            form.errors.as_json(),
            content_type="application/json",
            status=400,
        )

    def form_valid(self, form):
        status = form.cleaned_data["status"]
        self.payment.data["status"] = status
        self.payment.save()
        if status == TransactionStatuses.success:
            messages.success(self.request, _("Your payment was received"))
        else:
            messages.error(self.request, _("Your payment was not completed yet"))
        # TODO: mark order as paid if full sum is received
        return super().form_valid(form)

    def get_success_url(self):
        next_page = get_next_page(self.request)
        if next_page is not None:
            return next_page
        return super().get_success_url()

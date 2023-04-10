import logging

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import BaseFormView

from ...models import Payment
from ..utils import get_next_page, on_payment_failure
from .constants import TransactionStatuses
from .forms import CallbackForm

logger = logging.getLogger(__name__)


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
        allow_redirect = not form.cleaned_data.get(
            "notify"
        ) and not form.cleaned_data.get("callback")

        # register the reported Sisow status
        status = form.cleaned_data["status"]
        self.payment.data["status"] = status
        self.payment.save()

        logger.info(
            "Received information for Sisow payment %d, status: %s",
            self.payment.pk,
            status,
            extra={
                "payment": self.payment.pk,
                "status": status,
                "params": form.cleaned_data,
            },
        )

        fail_payment = status in (
            TransactionStatuses.expired,
            TransactionStatuses.cancelled,
            TransactionStatuses.failure,
            TransactionStatuses.reversed,
            TransactionStatuses.denied,
        )
        complete_payment = status == TransactionStatuses.success

        with transaction.atomic():
            if fail_payment:
                on_payment_failure(self.payment, self.request)
            elif complete_payment:
                self.payment.mark_paid()

        if not allow_redirect:
            return HttpResponse(b"processed", content_type="text/plain", status=200)

        if complete_payment:
            messages.success(self.request, _("Your payment was received"))
        elif fail_payment:
            messages.error(
                self.request, _("Your payment was not received (yet) - please retry.")
            )
        elif status == TransactionStatuses.open:
            messages.info(self.request, _("Your payment is being processed"))
        return super().form_valid(form)

    def get_success_url(self):
        return get_next_page(self.request) or super().get_success_url()

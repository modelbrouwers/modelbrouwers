from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

from furl import furl

from brouwers.emails.views import BaseEmailDebugView

from ..emails import render_order_confirmation as render_order_confirmation_email
from ..models import Order


class OrderConfirmationEmailView(
    SingleObjectMixin, BaseEmailDebugView
):  # pragma: no cover
    model = Order

    def get_email_content(self, mode):
        order = self.get_object()
        base_url = self.request.build_absolute_uri(reverse("index"))
        return render_order_confirmation_email(order, furl(base_url), mode=mode)

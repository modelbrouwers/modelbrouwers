from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Literal, assert_never

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.functional import Promise
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from furl import furl

from brouwers.general.fields import CountryField

from ..constants import DeliveryMethods, OrderEvents, OrderStatuses, PaymentStatuses
from .utils import get_random_reference

if TYPE_CHECKING:
    from .payments import Payment


class Address(models.Model):
    street = models.CharField(_("street name"), max_length=255)
    number = models.CharField(_("house number"), max_length=30, blank=True)
    postal_code = models.CharField(_("postal code"), max_length=50)
    city = models.CharField(_("city"), max_length=255)
    country = CountryField()

    # company details
    company = models.CharField(_("company"), max_length=255, blank=True)
    chamber_of_commerce = models.CharField(
        _("chamber of commerce number"), max_length=50, blank=True
    )

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        bits = [
            f"{self.street} {self.number}".strip(),
            self.postal_code,
            self.city,
            self.country,
        ]
        return ", ".join(bits)


def get_order_reference():
    """
    Generate a random but unique reference.
    """
    MAX_ATTEMPTS = 100  # ensure we have finite loops (while is evil)
    iterations = 0

    for _ in range(MAX_ATTEMPTS):  # noqa: F402
        iterations += 1
        reference = get_random_reference()
        exists = Order.objects.only("pk").filter(reference=reference).exists()
        if exists is False:
            return reference

    # loop ran all the way to the end without finding unused reference
    # (otherwise it would have returned)
    raise RuntimeError(
        f"Could not get a unused reference after {iterations} attempts!"
    )  # pragma: no cover


type OrderFieldsForUpdateEmail = Literal[
    "payment.status",
    "status",
    "track_and_trace_code",
    "track_and_trace_link",
]


class Order(models.Model):
    cart = models.OneToOneField(
        "Cart", on_delete=models.PROTECT, verbose_name=_("shopping cart")
    )
    status = models.CharField(_("status"), max_length=50, choices=OrderStatuses.choices)
    reference = models.CharField(
        _("reference"),
        max_length=16,
        unique=True,
        default=get_order_reference,
        help_text=_("A unique order reference"),
    )
    # TODO: add django-privates and field for invoices

    # personal details
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    email = models.EmailField(_("email"))
    phone = models.CharField(_("phone number"), max_length=100, blank=True)

    # addresses
    delivery_method = models.CharField(
        _("delivery method"),
        max_length=20,
        choices=DeliveryMethods.choices,
    )
    delivery_address = models.OneToOneField(
        "Address",
        on_delete=models.PROTECT,
        related_name="delivery_order",
        help_text=_("Address for delivery"),
        blank=True,
        null=True,
    )
    invoice_address = models.OneToOneField(
        "Address",
        on_delete=models.SET_NULL,
        related_name="invoice_order",
        blank=True,
        null=True,
    )

    # metadata
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)
    language = models.CharField(
        _("language"), max_length=10, default="nl", choices=settings.LANGUAGES
    )

    shipping_costs = models.DecimalField(
        _("shipping costs"),
        decimal_places=2,
        max_digits=6,
        blank=True,
        null=True,
    )
    track_and_trace_code = models.CharField(
        _("track and trace code"),
        max_length=100,
        blank=True,
        help_text=_(
            "If available, the track and trace code for the client to follow their "
            "parcel."
        ),
    )
    track_and_trace_link = models.URLField(
        _("track and trace link"),
        max_length=512,
        blank=True,
        help_text=_(
            "If available, the clickable track and trace link for the client to follow "
            "their parcel. If both the link and code are provided, the link will be "
            "displayed in the email."
        ),
    )

    payment: Payment
    orderevent_set: models.QuerySet[OrderEvent]

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        constraints = [
            models.CheckConstraint(
                name="delivery_address_when_shipping",
                check=(
                    Q(
                        delivery_method=DeliveryMethods.mail,
                        delivery_address__isnull=False,
                    )
                    | ~Q(delivery_method=DeliveryMethods.mail)
                ),
                violation_error_message=_(
                    "A delivery address must be specified when deliverying via mail."
                ),
            )
        ]

    def __str__(self):
        return _("Order {pk}").format(pk=self.pk)

    @staticmethod
    def get_changed_fields(
        order_old: Order, order_new: Order
    ) -> Sequence[OrderFieldsForUpdateEmail]:
        from .payments import Payment

        attrs: list[OrderFieldsForUpdateEmail] = []
        if order_new.status != order_old.status:
            attrs.append("status")
        try:
            if order_new.payment.status != order_old.payment.status:
                attrs.append("payment.status")
        except Payment.DoesNotExist:
            pass
        if order_new.track_and_trace_code != order_old.track_and_trace_code:
            attrs.append("track_and_trace_code")
        if order_new.track_and_trace_link != order_old.track_and_trace_link:
            attrs.append("track_and_trace_link")
        return attrs

    @property
    def is_actionable(self) -> bool:
        if self.payment.status != PaymentStatuses.completed:
            return False

        if self.status == OrderStatuses.received:
            return True

        return False

    def get_full_name(self) -> str:
        bits = [self.first_name, self.last_name]
        return " ".join(bits).strip()

    def get_confirmation_link(self) -> str:
        path = reverse("shop:checkout", kwargs={"path": "confirmation"})
        return furl(path).set({"orderId": self.pk}).url


class OrderEvent(models.Model):
    """
    Event that happened in relation to a particular order.

    All events together build up a timeline/history of an entire order.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("order"))
    timestamp = models.DateTimeField(
        _("timestamp"),
        auto_now_add=True,
        help_text=_("Moment in time when the event occurred."),
    )
    event = models.CharField(_("event type"), max_length=50, choices=OrderEvents)
    event_data = models.JSONField(
        _("event data"),
        null=True,
        blank=True,
        help_text=_("Additional data relevant for the selected event type."),
    )

    get_event_display: Callable[[], str]

    class Meta:
        verbose_name = _("order event")
        verbose_name_plural = _("order events")

    def __str__(self) -> str:
        return _("{timestamp}: {order} - {event}").format(
            timestamp=self.timestamp.isoformat(),
            order=self.order.reference if self.order else "(-)",
            event=self.get_event_display(),
        )

    def get_description(self) -> str | Promise:
        """
        Return the event description with all necessary context.
        """
        event = OrderEvents(self.event)
        match event:
            case OrderEvents.placed:
                return self.get_event_display()
            case OrderEvents.status_changed:
                old_status = OrderStatuses(self.event_data["old"])
                new_status = OrderStatuses(self.event_data["new"])
                return _("Status changed from '{old}' to '{new}'").format(
                    old=old_status.label.lower(),
                    new=new_status.label.lower(),
                )
            case OrderEvents.payment_status_changed:
                old_status = PaymentStatuses(self.event_data["old"])
                new_status = PaymentStatuses(self.event_data["new"])
                return _("Payment status changed from '{old}' to '{new}'").format(
                    old=old_status.label.lower(),
                    new=new_status.label.lower(),
                )
            case OrderEvents.email_sent:
                return format_html(
                    "Email sent to <a href=\"mailto:{to}\">{to}</a> with subject '{subject}'",
                    to=self.event_data["to"],
                    subject=self.event_data["subject"],
                )
            case _:  # pragma: no cover
                assert_never(event)

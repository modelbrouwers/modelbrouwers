from decimal import Decimal
from typing import Literal, cast

from django.conf import settings
from django.template.loader import get_template
from django.utils import timezone, translation
from django.utils.translation import gettext as _

from furl import furl
from mail_cleaner.mail import send_mail_plus
from mail_cleaner.sanitizer import sanitize_content
from mail_cleaner.text import strip_tags_plus

from .constants import TWO_DIGITS
from .models import Order, ShopConfiguration


def send_order_confirmation_email(order: Order, base_url: str) -> None:
    config = cast(ShopConfiguration, ShopConfiguration.get_solo())
    base = furl(base_url)
    if not base.host:  # pragma: no cover
        raise ValueError("Unsupported base URL provided")
    allowlist = [base.host]

    subject = _("Modelbrouwers - order {order_number}").format(
        order_number=order.reference
    )
    html_body = sanitize_content(
        render_order_confirmation(order=order, base=base, mode="html"),
        allowlist=allowlist,
    )
    text_body = sanitize_content(
        render_order_confirmation(order=order, base=base, mode="text"),
        allowlist=allowlist,
    )

    send_mail_plus(
        subject,
        message=text_body,
        from_email=config.from_email or settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.email],
        html_message=html_body,
        headers={"Content-Language": order.language},
    )


def render_order_confirmation(
    order: Order, base: furl, mode: Literal["text", "html"]
) -> str:
    """
    Render the email body for an order confirmation.
    """
    html_template = get_template("shop/emails/order_confirmation.html")

    payment = order.payment if hasattr(order, "payment") else None

    products = order.cart.snapshot_data["products"]
    total_vat = sum(
        (
            Decimal(prod["amount"]) * Decimal(prod["vat"]) * Decimal(prod["price"])
            for prod in products
        ),
        Decimal(0),
    )

    with translation.override(order.language):
        context = {
            "order": {
                "reference": order.reference,
                "link": order.get_confirmation_link(),  # TODO -> make absolute URL
                "date": timezone.localtime(
                    order.created
                ).date(),  # TODO: store and use user timezone
                "payment_method": payment.payment_method.name if payment else None,
                "payment_status": payment.get_status_display() if payment else None,
                # "shipping_method": "TODO",
            },
            "contact": {
                "email": order.email,
                "phone": order.phone,
            },
            "instructions": "",  # TODO: include payment method instructions if present
            "customer_name": order.get_full_name(),
            "delivery_address": order.delivery_address,
            "invoice_address": order.invoice_address or order.delivery_address,
            "products": products,
            "total": (total := Decimal(order.cart.snapshot_data["total"])),
            "subtotal": (total - total_vat).quantize(TWO_DIGITS),
            "total_vat": total_vat.quantize(TWO_DIGITS),
        }
        html = html_template.render(context)
    return html

from decimal import Decimal

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ..constants import TWO_DIGITS, CartStatuses
from ..managers import CartQuerySet


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="carts",
    )
    status = models.CharField(
        _("status"),
        max_length=50,
        choices=CartStatuses.choices,
        default=CartStatuses.open,
    )
    snapshot_data = models.JSONField(
        _("snapshot data"),
        encoder=DjangoJSONEncoder,
        help_text=_("Snapshot of order information with frozen prices."),
        null=True,
    )

    objects = CartQuerySet.as_manager()

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")

    def get_absolute_url(self):
        return reverse("shop:cart-detail", kwargs={"pk": self.pk})

    @property
    def total(self) -> Decimal:
        """
        Total price of all the products in the cart
        """
        return sum(product.total for product in self.products.all())

    def save_snapshot(self) -> None:
        """
        Freeze all the cart product information for archiving purposes.

        This prevents historic orders and their prices/totals being mutated when product
        prices eventually are updated/indexed, or even completely removed.

        TODO: include reduction/benefits information
        """
        data = {"products": [], "total": self.total}
        for cart_product in self.products.all():
            data["products"].append(
                {
                    "id": cart_product.product.id,
                    "name": str(cart_product.product),
                    "amount": cart_product.amount,
                    "price": cart_product.product.price,
                    "vat": cart_product.product.vat,
                    "total": cart_product.total,
                }
            )

        self.snapshot_data = data
        self.save(update_fields=["snapshot_data"])


class CartProduct(models.Model):
    product = models.ForeignKey(
        "Product",
        related_name="cart_products",
        on_delete=models.CASCADE,
    )
    cart = models.ForeignKey("Cart", related_name="products", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(_("amount"), default=1)

    class Meta:
        verbose_name = _("cart product")
        verbose_name_plural = _("cart products")

    def __str__(self):
        return self.product.name or self.product.name_nl

    @property
    def total(self) -> Decimal:
        """
        Total price for the amount of products
        """
        return (self.product.price * self.amount).quantize(TWO_DIGITS)

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ..constants import TWO_DIGITS, CartStatuses
from ..managers import CartQuerySet


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='carts')
    status = models.CharField(_('status'), max_length=10, choices=CartStatuses.choices, default=CartStatuses.open)

    objects = CartQuerySet.as_manager()

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def get_absolute_url(self):
        return reverse('shop:cart-detail', kwargs={'pk': self.pk})

    @property
    def total(self):
        """
        Total price of all the products in the cart
        """
        return sum(product.total for product in self.products.all())


@python_2_unicode_compatible
class CartProduct(models.Model):
    product = models.ForeignKey('Product', related_name='cart_products')
    cart = models.ForeignKey('Cart', related_name='products')
    amount = models.PositiveIntegerField(_('amount'), default=1)

    class Meta:
        verbose_name = _('cart product')
        verbose_name_plural = _('cart products')

    def __str__(self):
        return self.product.name or self.product.name_nl

    @property
    def total(self):
        """
        Total price for the amount of products
        """
        return (self.product.price * self.amount).quantize(TWO_DIGITS)

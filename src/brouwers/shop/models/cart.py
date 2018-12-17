from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ..constants import CartStatuses


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(_('status'), max_length=10, choices=CartStatuses.choices)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def get_absolute_url(self):
        return reverse('shop:cart-detail', kwargs={'pk': self.pk})


@python_2_unicode_compatible
class CartProduct(models.Model):
    product = models.ForeignKey('Product', related_name='cart_products')
    cart = models.ForeignKey('Cart', related_name='cart_products')
    amount = models.PositiveIntegerField(_('amount'), default=1)

    class Meta:
        verbose_name = _('cart product')
        verbose_name_plural = _('cart products')

    def __str__(self):
        return self.product.name or self.product.name_nl

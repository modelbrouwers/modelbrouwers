from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField


class Product(models.Model):
    name = models.CharField(_('name'), max_length=30)
    slug = AutoSlugField(_('slug'), unique=True, populate_from='name')
    brand = models.ForeignKey('ProductBrand', null=True, blank=True, on_delete=models.PROTECT)
    model_name = models.CharField(_('model name'), max_length=30)
    stock = models.PositiveIntegerField(_('stock'), max_length=30, help_text=_('Number of items in stock'))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, default=0)
    vat = models.IntegerField(_('vat'), default=0)
    description = RichTextField(blank=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', null=True, blank=True)
    image = models.ImageField(_('product image'), upload_to='shop/product/')

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
        ordering = ['name']


class ProductBrand(models.Model):
    name = models.CharField(_('name'), max_length=30)
    slug = AutoSlugField(_('slug'), unique=True, populate_from='name')
    logo = models.ImageField(_('logo'), upload_to='images/product_brand_logos/', blank=True)

    class Meta:
        verbose_name = _('product brand')
        verbose_name_plural = _('product brands')
        ordering = ['name']

    def __str__(self):
        return self.name

from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

DEFAULT_RATING = 50
MAX_RATING = 100
MIN_RATING = 0


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = AutoSlugField(_('slug'), unique=True, populate_from='name')
    brand = models.ForeignKey('ProductBrand', null=True, blank=True, on_delete=models.PROTECT)
    model_name = models.CharField(_('model name'), max_length=30)
    stock = models.PositiveIntegerField(_('stock'), help_text=_('Number of items in stock'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(_('vat'), max_digits=3, decimal_places=2, default=0)
    description = RichTextField(blank=True)
    seo_keyword = models.CharField(_('seo keyword'), max_length=100, null=True, blank=True)
    length = models.DecimalField(_('length'), max_digits=10, decimal_places=2, default=0)
    width = models.DecimalField(_('width'), max_digits=10, decimal_places=2, default=0)
    height = models.DecimalField(_('height'), max_digits=10, decimal_places=2, default=0)
    weight = models.DecimalField(_('weight'), max_digits=10, decimal_places=2, default=0)
    related_products = models.ManyToManyField('self', blank=True)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.PROTECT)
    manufacturer = models.ForeignKey('ProductManufacturer', related_name='products', null=True, blank=True,
                                     on_delete=models.PROTECT)
    tags = TaggableManager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', null=True, blank=True)
    image = models.ImageField(_('product image'), upload_to='shop/product/')

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')


@python_2_unicode_compatible
class ProductBrand(models.Model):
    name = models.CharField(_('name'), max_length=30)
    slug = AutoSlugField(_('slug'), unique=True, populate_from='name')
    logo = models.ImageField(_('logo'), upload_to='images/product_brand_logos/', blank=True)

    class Meta:
        verbose_name = _('product brand')
        verbose_name_plural = _('product brands')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProductReview(models.Model):
    product = models.ForeignKey('Product', related_name='reviews', null=True, blank=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = RichTextField()
    rating = models.PositiveSmallIntegerField(
        _('rating'), default=DEFAULT_RATING,
        validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)]
    )
    submitted_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('product review')
        verbose_name_plural = _('product reviews')

    def __str__(self):
        return _('Review: %(product)s by %(user)s') % {
            'kit': self.product.name,
            'user': self.reviewer.username,
        }


@python_2_unicode_compatible
class ProductManufacturer(models.Model):
    name = models.CharField(_('manufacturer'), max_length=30)

    class Meta:
        verbose_name = _('product manufacturer')
        verbose_name_plural = _('product manufacturers')

    def __str__(self):
        return self.name

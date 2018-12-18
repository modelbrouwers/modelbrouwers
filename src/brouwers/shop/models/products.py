from __future__ import unicode_literals

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

from ..constants import WeightUnits
from ..managers import ProductQuerySet

MAX_RATING = 5
MIN_RATING = 1


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = AutoSlugField(_('slug'), max_length=200, unique=True, populate_from='name')
    brand = models.ForeignKey('ProductBrand', null=True, blank=True, on_delete=models.PROTECT)
    model_name = models.CharField(_('model name'), max_length=30)
    stock = models.PositiveIntegerField(_('stock'), help_text=_('Number of items in stock'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(_('vat'), max_digits=3, decimal_places=2, default=0)
    description = RichTextField(blank=True)
    seo_keyword = models.CharField(_('seo keyword'), max_length=200, null=True, blank=True)
    image = models.ImageField(_('image'), upload_to='shop/product/', null=True, blank=True)

    # dimensional data
    length = models.DecimalField(_('length'), max_digits=10, decimal_places=2, default=0)
    width = models.DecimalField(_('width'), max_digits=10, decimal_places=2, default=0)
    height = models.DecimalField(_('height'), max_digits=10, decimal_places=2, default=0)
    # TODO: need length unit?

    weight = models.DecimalField(_('weight'), max_digits=10, decimal_places=2, default=0)
    weight_unit = models.CharField(_('weight unit'), max_length=10, choices=WeightUnits.choices)

    related_products = models.ManyToManyField('self', blank=True)
    categories = models.ManyToManyField('Category', related_name='products')
    manufacturer = models.ForeignKey('ProductManufacturer', related_name='products', null=True, blank=True,
                                     on_delete=models.PROTECT)
    tags = TaggableManager()
    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name or self.name_nl

    def get_absolute_url(self):
        return reverse('shop:product-detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        image = self.image

        if not image:
            return static('images/shop/placeholder.gif')
        return image.url


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
    product = models.ForeignKey('Product', related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        _('rating'), validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)]
    )
    submitted_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('product review')
        verbose_name_plural = _('product reviews')

    def __str__(self):
        return _('Review: %(product)s by %(user)s') % {
            'product': self.product.name,
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

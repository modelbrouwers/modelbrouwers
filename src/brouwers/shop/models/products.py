from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

from ..constants import LengthUnits, WeightUnits

MAX_RATING = 5
MIN_RATING = 1


class Product(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    model_name = models.CharField(_("model name"), max_length=30)
    stock = models.PositiveIntegerField(
        _("stock"), help_text=_("Number of items in stock")
    )
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(_("vat"), max_digits=3, decimal_places=2, default=0)
    description = RichTextField(blank=True)
    image = models.ImageField(
        _("image"), upload_to="shop/product/", null=True, blank=True
    )

    # SEO
    meta_description = models.TextField(
        _("meta description"),
        blank=True,
        help_text=_(
            "If filled, populates the description meta tag for SEO purposes. "
            "If left blank, then the HTML tags are stripped from the regular "
            "description field and this content is used."
        ),
    )

    # dimensional data
    length = models.DecimalField(
        _("length"), max_digits=10, decimal_places=2, default=0
    )
    width = models.DecimalField(_("width"), max_digits=10, decimal_places=2, default=0)
    height = models.DecimalField(
        _("height"), max_digits=10, decimal_places=2, default=0
    )
    length_unit = models.CharField(
        _("length unit"),
        max_length=10,
        choices=LengthUnits.choices,
        default=LengthUnits.cm,
    )

    weight = models.DecimalField(
        _("weight"), max_digits=10, decimal_places=2, default=0
    )
    weight_unit = models.CharField(
        _("weight unit"),
        max_length=10,
        choices=WeightUnits.choices,
        default=WeightUnits.gram,
    )

    related_products = models.ManyToManyField("self", blank=True)
    categories = models.ManyToManyField("Category", related_name="products")
    manufacturer = models.ForeignKey(
        "ProductManufacturer",
        related_name="products",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Inactive products do not show up on the site"),
    )
    tags = TaggableManager()

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:catalogue", kwargs={"path": self.slug})

    def get_image_url(self):
        image = self.image

        if not image:
            return static("images/shop/placeholder.gif")
        return image.url

    @property
    def json_ld(self):
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "description": strip_tags(self.description),
            "name": self.name,
            "sku": self.model_name,
            "offers": {
                "@type": "Offer",
                "availability": (
                    "https://schema.org/InStock"
                    if self.stock
                    else "https://schema.org/OutOfStock"
                ),
                "price": str(self.price),
                "priceCurrency": "EUR",
            },
            "url": self.get_absolute_url(),
        }
        if self.image:
            schema["image"] = self.image.url
        return schema


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product",
        related_name="images",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(_("product image"), upload_to="shop/product/")

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


class ProductManufacturer(models.Model):
    name = models.CharField(_("manufacturer"), max_length=30)

    class Meta:
        verbose_name = _("product manufacturer")
        verbose_name_plural = _("product manufacturers")

    def __str__(self):
        return self.name

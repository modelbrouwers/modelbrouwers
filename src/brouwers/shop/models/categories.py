from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from treebeard.mp_tree import MP_Node


class Category(MP_Node):
    name = models.CharField(_("name"), max_length=100)
    slug = AutoSlugField(_("slug"), unique=True, populate_from="name", editable=True)
    image = models.ImageField(_("thumbnail"), upload_to="shop/category/", blank=True)
    enabled = models.BooleanField(_("enabled"), default=True)

    # SEO
    meta_description = models.TextField(
        _("meta description"),
        blank=True,
        help_text=_("If filled, populates the description meta tag for SEO purposes."),
    )

    node_order_by = ["name"]

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category-detail", kwargs={"slug": self.slug})


class CategoryCarouselImage(models.Model):
    title = models.CharField(_("title"), max_length=100)
    image = models.ImageField(_("category carousel image"), upload_to="shop/category/")
    visible = models.BooleanField(_("visible"), default=True)

    class Meta:
        verbose_name = _("category carousel image")
        verbose_name_plural = _("category carousel images")

    def __str__(self):
        return self.title

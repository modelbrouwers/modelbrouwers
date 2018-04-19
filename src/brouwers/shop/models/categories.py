# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from treebeard.mp_tree import MP_Node


class Category(MP_Node):
    name = models.CharField(_('name'), max_length=30)
    slug = AutoSlugField(_('slug'), unique=True, populate_from='name')
    image = models.ImageField(_('thumbnail'), upload_to='shop/category/', blank=True)
    seo_keyword = models.CharField(_('seo keyword'), max_length=100, null=True, blank=True)
    enabled = models.BooleanField(_('enabled'), default=True)

    node_order_by = ['name']

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

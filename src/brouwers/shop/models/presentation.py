# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class HomepageCategory(models.Model):
    main_category = models.OneToOneField(
        'Category',
        related_name='homepage_categories',
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField(_('order'), help_text=_('Order in which to display category on the homepage'))

    class Meta:
        verbose_name = _('homepage category')
        verbose_name_plural = _('homepage categories')

    def __str__(self):
        return self.main_category.name


@python_2_unicode_compatible
class HomepageCategoryChild(models.Model):
    parent = models.ForeignKey('HomepageCategory', related_name='children', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='homepage_category_children', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_('order'), help_text=_('Order in which to display category on the homepage'))

    class Meta:
        verbose_name = _('homepage category child')
        verbose_name_plural = _('homepage category children')

    def __str__(self):
        return self.category.name

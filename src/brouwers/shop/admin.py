# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'seo_keyword', 'enabled')
    list_filter = ('name', 'seo_keyword', 'enabled')
    search_fields = ('name', 'seo_keyword')

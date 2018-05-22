# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, ListView

from brouwers.shop.models import Category, Product


class IndexView(ListView):
    queryset = Category.get_tree().filter(depth=1)
    context_object_name = 'categories'
    template_name = 'shop/index.html'

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, ListView

from brouwers.shop.models import Category, Product, CategoryCarouselImage


class IndexView(ListView):
    queryset = Category.get_tree().filter(depth=1)
    context_object_name = 'categories'
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['carousel_images'] = CategoryCarouselImage.objects.filter(visible=True)
        return context

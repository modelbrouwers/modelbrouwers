# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import ModelFormMixin

from .forms import ProductReviewForm
from .models import Category, CategoryCarouselImage, HomepageCategory, Product


class IndexView(ListView):
    queryset = HomepageCategory.objects.all().order_by('order')
    context_object_name = 'categories'
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['carousel_images'] = CategoryCarouselImage.objects.filter(visible=True)
        return context


class CategoryDetailView(DetailView):
    context_object_name = 'category'
    template_name = 'shop/category_detail.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.get_tree().filter(depth=1, enabled=True)
        return context


class ProductDetailView(ModelFormMixin, DetailView):
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    model = Product
    form_class = ProductReviewForm

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.get_tree().filter(depth=1, enabled=True)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse('shop:product-detail', kwargs={'slug': self.object.product.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form.instance.reviewer = self.request.user
        form.instance.product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if form.is_valid():
            return redirect(self.get_success_url())
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

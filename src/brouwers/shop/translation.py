from modeltranslation.translator import TranslationOptions, register

from .models import Category, PaymentMethod, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug', 'seo_keyword')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'slug', 'seo_keyword', 'model_name', 'description')


@register(PaymentMethod)
class PaymentMethodTranslationOptions(TranslationOptions):
    fields = ('name',)

from modeltranslation.translator import register, TranslationOptions
from .models import Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug', 'seo_keyword')

from modeltranslation.translator import TranslationOptions, register

from .models import Category, PaymentMethod, Product, ShopConfiguration


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "slug", "meta_description")


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "slug", "meta_description", "model_name", "description")


@register(PaymentMethod)
class PaymentMethodTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(ShopConfiguration)
class ShopConfigurationTranslationOptions(TranslationOptions):
    fields = ("bank_transfer_instructions",)

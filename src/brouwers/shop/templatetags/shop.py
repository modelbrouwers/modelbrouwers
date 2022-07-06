from django.template import Library

from ..models import Category

register = Library()


@register.simple_tag
def category_tree(**extra_filters):
    default_filters = {"enabled": True, "depth__lte": 2}
    filters = {**default_filters, **extra_filters}
    qs = Category.get_tree().filter(**filters)
    return Category.get_annotated_list_qs(qs)


@register.simple_tag
def is_descendant_of(node1, node2) -> bool:
    return node1.is_descendant_of(node2)

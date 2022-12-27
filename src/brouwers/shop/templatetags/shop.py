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
def is_in_branch(node1, node2) -> bool:
    """
    Check whether node1 and node2 are in the same branch.

    Node 1 should be the node expected to be closer to the leaf, while node 2 is closer
    to the root.
    """
    if node1 == node2:
        return True
    return node1.is_descendant_of(node2)

import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import _json_script_escapes, format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def startswith(value, arg):
    """Usage, {% if value|starts_with:"arg" %}"""
    return value.startswith(arg)


@register.filter("columns")
def columns(items, columns=4):
    """
    :param items: typically an iterable of forms
    """
    if items:
        return [items[i : i + columns] for i in range(0, len(items), columns)]
    return None


@register.filter("rows")
def rows(items, rows=4):
    """
    Transform the list so that it's evenly spread across n rows.
    """
    if items:
        res = [[] for i in range(rows)]
        for i, item in enumerate(items):
            res[i % rows].append(item)
        return res
    return None


@register.inclusion_tag("general/includes/rating.html")
def review_rating(rating_pct, num_stars=5, max_rating=100):
    if not rating_pct:
        return {"full": [], "half": False, "open": range(num_stars)}
    full = int(rating_pct / max_rating * num_stars)
    empty = int((max_rating - rating_pct) / max_rating * num_stars)

    return {
        "full": range(full),
        "half": (full + empty) != num_stars,
        "open": range(empty),
    }


@register.filter(is_safe=True)
def json_ld_script(value):
    json_str = json.dumps(value, cls=DjangoJSONEncoder).translate(_json_script_escapes)
    return format_html(
        '<script type="application/ld+json">{}</script>',
        mark_safe(json_str),
    )

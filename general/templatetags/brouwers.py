from django import template


register = template.Library()


@register.filter
def startswith(value, arg):
    """Usage, {% if value|starts_with:"arg" %} """
    return value.startswith(arg)


@register.filter('columns')
def columns(items, columns=4):
    """
    :param items: typically an iterable of forms
    """
    if items:
        return [items[i:i+columns] for i in range(0, len(items), columns)]
    return None

@register.filter('rows')
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

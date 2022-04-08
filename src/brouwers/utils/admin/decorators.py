from functools import wraps

from django.urls import reverse
from django.utils.html import format_html_join


def get_urlname(obj):
    app_label, model_name = obj._meta.app_label, obj._meta.model_name
    return "admin:{}_{}_change".format(app_label, model_name)


def get_reverse_args(obj, *arg_names):
    args = [getattr(obj, arg) for arg in arg_names]
    return args


def get_repr_attr(obj, attr=None):
    if attr is None:
        return obj
    attrs = attr.split(".")
    value = obj
    for attr in attrs:
        value = getattr(value, attr)
    return value


def related_list(short_description=None, repr_attr=None):
    """
    Decorates a modeladmin method to display a list of related links, non-clickable.
    """

    def decorator(method):
        method.allow_tags = True
        if short_description:
            method.short_description = short_description

        @wraps(method)
        def f(*args, **kwargs):
            related_qs = method(*args, **kwargs)
            return ", ".join(
                ["{}".format(get_repr_attr(rel, repr_attr)) for rel in related_qs]
            )

        return f

    return decorator


def link_list(urlname=None, short_description=None, reverse_args=None):
    """
    Decorates a modeladmin method to display a list of related links.

    :param urlname: optional, by default it will take the related objects change url
    :param short_description: text to use as column header, optional

    Usage:

    >>> class MyAdmin(admin.ModelAdmin):
            list_display = ('related_objects',)

            @link_list('admin:myapp_relatedobject_change', short_description='my related objects')
            def related_objects(self, obj):
                return obj.relatedobject_set.all()

    The ModelAdmin method then returns a comma-separated list of clickable links.
    """
    if reverse_args is None:
        reverse_args = ["pk"]

    def decorator(method):
        if short_description:
            method.short_description = short_description

        @wraps(method)
        def f(*args, **kwargs):
            related_qs = method(*args, **kwargs)
            args_generator = (
                (
                    reverse(
                        urlname or get_urlname(rel),
                        args=get_reverse_args(rel, *reverse_args),
                    ),
                    str(rel),
                )
                for rel in related_qs
            )
            return format_html_join(", ", '<a href="{0}">{1}</a>', args_generator)

        return f

    return decorator

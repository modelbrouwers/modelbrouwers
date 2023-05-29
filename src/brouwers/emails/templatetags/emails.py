from django.template import Library

from furl import furl

register = Library()


@register.simple_tag(takes_context=True)
def absolute_url(context, path: str) -> str:
    if not (base := context.get("base")):  # pragma: no cover
        raise ValueError(
            "The 'base' context variable must be provided with a fully "
            "qualified URL to use as root."
        )
    url = furl(base) if not isinstance(base, furl) else base.copy()
    url.set(path=path)
    return url.url

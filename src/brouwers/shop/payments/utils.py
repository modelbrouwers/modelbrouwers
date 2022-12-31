from typing import Optional

from django.http import HttpRequest
from django.utils.http import url_has_allowed_host_and_scheme


def get_next_page(request: HttpRequest, next_param="next") -> Optional[str]:
    if not (next_page := request.GET.get(next_param)):
        return None

    url_is_safe = url_has_allowed_host_and_scheme(
        url=next_page,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    )
    if not url_is_safe:
        return None

    return next_page

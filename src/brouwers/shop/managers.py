from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q, QuerySet

from .constants import CART_SESSION_KEY, CartStatuses

if TYPE_CHECKING:
    from .models import Cart


class CartQuerySet(QuerySet["Cart"]):
    def open(self):
        """
        Filter carts by 'open' status.
        """
        return self.filter(status=CartStatuses.open)

    def for_request(self, request) -> QuerySet:
        q = Q()
        if cart_id := request.session.get(CART_SESSION_KEY):
            q |= Q(id=cart_id)

        if request.user.is_authenticated:
            q |= Q(user=request.user)

        if not q:
            return self.none()

        return self.filter(q)

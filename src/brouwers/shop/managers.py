from django.db.models import Q, QuerySet

from .constants import CART_SESSION_KEY, CartStatuses


class CartQuerySet(QuerySet):
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

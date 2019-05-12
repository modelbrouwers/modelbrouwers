from django.db.models import Avg, Q, QuerySet

from .constants import CartStatuses


class ProductQuerySet(QuerySet):

    def annotate_mean_rating(self):
        return self.annotate(
            avg_rating=Avg('reviews__rating')
        )


class CartQuerySet(QuerySet):

    def open(self):
        """
        Filter carts by 'open' status.
        """
        return self.filter(status=CartStatuses.open)

    def for_request(self, request):
        return self.filter(Q(user=request.user) | Q(id=request.session.get('cart_id')))

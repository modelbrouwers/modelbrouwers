from django.db.models import Avg, QuerySet


class ProductQuerySet(QuerySet):

    def annotate_mean_rating(self):
        return self.annotate(
            avg_rating=Avg('reviews__rating')
        )

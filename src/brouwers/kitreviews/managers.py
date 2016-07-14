from django.db.models import Avg, F, QuerySet


class KitReviewQuerySet(QuerySet):

    def annotate_mean_rating(self):
        from .models import MAX_RATING
        return self.annotate(
            avg_rating=Avg('ratings__rating')
        ).annotate(rating_pct=F('avg_rating') / MAX_RATING * 100)

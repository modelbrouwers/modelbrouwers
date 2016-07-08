from django.db.models import Avg, Count, Case, F, When, IntegerField, QuerySet


class KitReviewQuerySet(QuerySet):

    def with_votes(self):
        from .models import VoteTypes
        return self.annotate(
            votes_pos=Count(Case(
                When(kitreviewvote__vote=VoteTypes.positive, then=1),
                output_field=IntegerField()
            )),
            votes_neg=Count(Case(
                When(kitreviewvote__vote=VoteTypes.negative, then=1),
                output_field=IntegerField()
            )),
        ).annotate(
            votes_total=F('votes_pos') + F('votes_neg')
        )

    def annotate_mean_rating(self):
        from .models import MAX_RATING
        return self.annotate(
            avg_rating=Avg('ratings__rating')
        ).annotate(rating_pct=F('avg_rating') / MAX_RATING * 100)

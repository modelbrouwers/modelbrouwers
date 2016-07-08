from __future__ import division

from django.template import Library

register = Library()


@register.inclusion_tag('kitreviews/includes/review_preview.html')
def render_review_preview(review, show_ratings=True):
    return {
        'review': review,
        'show_ratings': show_ratings,
    }


@register.inclusion_tag('kitreviews/includes/rating.html')
def review_rating(rating_pct, num_stars=5):
    full = int(rating_pct / 100 * num_stars)
    empty = int((100 - rating_pct) / 100 * num_stars)
    return {
        'full': range(full),
        'half': (full + empty) != num_stars,
        'open': range(empty),
    }

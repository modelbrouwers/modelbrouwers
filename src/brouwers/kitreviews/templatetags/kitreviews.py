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
    if not rating_pct:
        return {
            'full': [],
            'half': False,
            'open': range(num_stars)
        }
    full = int(rating_pct / 100 * num_stars)
    empty = int((100 - rating_pct) / 100 * num_stars)
    return {
        'full': range(full),
        'half': (full + empty) != num_stars,
        'open': range(empty),
    }


@register.filter
def rating_class(rating):
    """
    Outputs the Bootstrap CSS class for the review rating based on the range.
    """
    try:
        rating = float(rating)
    except ValueError:
        return ""

    if rating >= 80:
        return 'success'
    if rating >= 50:
        return 'info'
    if rating >= 20:
        return 'warning'
    return 'danger'

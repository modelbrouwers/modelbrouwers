from __future__ import division

from django.template import Library

register = Library()


@register.inclusion_tag("kitreviews/includes/review_preview.html")
def render_review_preview(review, show_ratings=True):
    return {
        "review": review,
        "show_ratings": show_ratings,
    }


@register.inclusion_tag("kitreviews/includes/detailed_ratings.html")
def detailed_ratings(review, is_preview=False):
    return {
        "ratings": review.ratings.all(),
        "is_preview": is_preview,
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
        return "success"
    if rating >= 50:
        return "info"
    if rating >= 20:
        return "warning"
    return "danger"

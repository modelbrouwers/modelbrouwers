from django.template import Library

register = Library()


@register.inclusion_tag('kitreviews/includes/review_preview.html')
def render_review_preview(review, show_ratings=True):
    return {
        'review': review,
        'show_ratings': show_ratings,
    }

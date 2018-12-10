from django import forms

from brouwers.shop.models import ProductReview, MAX_RATING, MIN_RATING
from brouwers.utils.widgets import StarRatingSelect


class ProductReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(n, n) for n in range(MIN_RATING, MAX_RATING + 1)], widget=StarRatingSelect())

    class Meta:
        model = ProductReview
        fields = ['rating', 'text']

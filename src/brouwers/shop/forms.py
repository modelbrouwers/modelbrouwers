from django import forms
from django.utils.translation import gettext_lazy as _

from brouwers.utils.widgets import StarRatingSelect

from .models import MAX_RATING, MIN_RATING, ProductReview


class ProductReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(n, n) for n in range(MIN_RATING, MAX_RATING + 1)],
        widget=StarRatingSelect(),
    )

    class Meta:
        model = ProductReview
        fields = ["rating", "text"]

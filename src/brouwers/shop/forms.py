from django import forms

from brouwers.shop.models import ProductReview, MAX_RATING, MIN_RATING
from brouwers.utils.widgets import StarRatingSelect


class ProductReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())
    rating = forms.ChoiceField(choices=[(n, n) for n in range(MIN_RATING, MAX_RATING + 1)], widget=StarRatingSelect())

    class Meta:
        model = ProductReview
        fields = ['rating', 'text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductReviewForm, self).__init__(*args, **kwargs)

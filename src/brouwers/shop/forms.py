from django import forms

from brouwers.shop.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = ProductReview
        fields = ['rating', 'text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductReviewForm, self).__init__(*args, **kwargs)

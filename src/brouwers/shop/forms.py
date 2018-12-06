from django import forms
from brouwers.shop.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = ProductReview
        fields = [
            'reviewer',
            'rating'
        ]

    def save(self, *args, **kwargs):
        self.instance.reviewer = self.user
        return super(ProductReviewForm, self).save(*args, **kwargs)

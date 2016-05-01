from django.views.generic import DetailView, ListView

from extra_views import InlineFormSet, CreateWithInlinesView, NamedFormsetsMixin

from brouwers.utils.views import LoginRequiredMixin
from .forms import KitReviewForm
from .models import KitReview, KitReviewProperty, KitReviewPropertyRating


class IndexView(ListView):
    queryset = KitReview.objects.order_by('-submitted_on')[:5]
    context_object_name = 'reviews'
    template_name = 'kitreviews/base.html'


class ReviewPropertyRatingInline(InlineFormSet):
    model = KitReviewPropertyRating

    @property
    def extra(self):
        return KitReviewProperty.objects.count()

    def get_initial(self):
        return [{'prop': prop} for prop in KitReviewProperty.objects.all()]


class AddReview(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = KitReview
    template_name = 'kitreviews/add_review.html'
    form_class = KitReviewForm
    inlines = [ReviewPropertyRatingInline]
    inlines_names = ['properties']

    def get_form_kwargs(self):
        kwargs = super(AddReview, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class FindKit(DetailView):
    pass


class KitReviewDetail(DetailView):
    model = KitReview
    template_name = 'kitreviews/kitreview_detail.html'
    context_object_name = 'kit_review'

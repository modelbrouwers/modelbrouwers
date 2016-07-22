from django.db.models import Count, Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, FormView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from extra_views import InlineFormSet, CreateWithInlinesView, NamedFormsetsMixin

from brouwers.kits.models import ModelKit
from brouwers.utils.views import LoginRequiredMixin
from .forms import KitReviewForm, FindModelKitForm, KitReviewPropertyRatingForm
from .models import KitReview, KitReviewProperty, KitReviewPropertyRating


class IndexView(FormMixin, ListView):
    queryset = KitReview.objects.select_related(
        'reviewer', 'model_kit'
    ).annotate_mean_rating().order_by('-submitted_on')[:5]
    context_object_name = 'reviews'
    template_name = 'kitreviews/index.html'
    form_class = FindModelKitForm


class ReviewPropertyRatingInline(InlineFormSet):
    model = KitReviewPropertyRating
    form_class = KitReviewPropertyRatingForm

    @property
    def num_properties(self):
        if not hasattr(self, '_num_properties'):
            self._num_properties = KitReviewProperty.objects.count()
        return self._num_properties

    def get_factory_kwargs(self):
        kwargs = super(ReviewPropertyRatingInline, self).get_factory_kwargs()
        kwargs.update({
            'min_num': self.num_properties,
            'max_num': self.num_properties,
        })
        return kwargs

    @property
    def extra(self):
        return self.num_properties

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

    def get_initial(self):
        initial = super(AddReview, self).get_initial()
        if self.kwargs.get('slug'):
            initial['model_kit'] = get_object_or_404(ModelKit, slug=self.kwargs['slug'])
        return initial


class KitSearchView(FormView):
    template_name = 'kitreviews/find_kit.html'
    form_class = FindModelKitForm

    def get_form_kwargs(self):
        kwargs = super(KitSearchView, self).get_form_kwargs()
        if 'data' not in kwargs:
            kwargs['data'] = self.request.GET
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        kits = form.find_kits()
        kits = kits.annotate(num_reviews=Count('kitreview'))
        return self.render_to_response(self.get_context_data(kits=kits))


class ReviewListView(SingleObjectMixin, ListView):
    queryset = KitReview.objects.prefetch_related(
        Prefetch('ratings', queryset=KitReviewPropertyRating.objects.select_related('prop'))
    ).select_related('reviewer', 'album').annotate_mean_rating()
    queryset_kits = ModelKit.objects.select_related('brand', 'scale')
    template_name = 'kitreviews/kit_review_list.html'

    def get_queryset(self):
        self.object = kit = self.get_object(queryset=self.queryset_kits)
        return super(ReviewListView, self).get_queryset().filter(model_kit=kit)

    def get_context_data(self, **kwargs):
        kwargs['kit'] = self.object
        return super(ReviewListView, self).get_context_data(**kwargs)


class KitReviewDetail(DetailView):
    queryset = KitReview.objects.select_related('model_kit')
    template_name = 'kitreviews/kitreview_detail.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('kit', self.object.model_kit)
        kwargs['other_reviews'] = self.object.model_kit.kitreview_set.select_related(
            'reviewer', 'album'
        ).annotate_mean_rating().exclude(pk=self.object.pk)
        return super(KitReviewDetail, self).get_context_data(**kwargs)


class LegacyRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        try:
            review_id = int(self.request.GET.get('review'))
        except (ValueError, TypeError):
            raise Http404
        review = get_object_or_404(KitReview, legacy_id=review_id)
        return review.get_absolute_url()

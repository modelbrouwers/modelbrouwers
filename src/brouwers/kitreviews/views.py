from django.forms import modelform_factory
from django.views.generic import DetailView, ListView, FormView

from extra_views import InlineFormSet, CreateWithInlinesView, NamedFormsetsMixin

from brouwers.utils.forms import AlwaysChangedModelForm
from brouwers.utils.views import LoginRequiredMixin
from .forms import KitReviewForm, FindModelKitForm
from .models import KitReview, KitReviewProperty, KitReviewPropertyRating
from brouwers.kits.models import ModelKit


class IndexView(ListView):
    queryset = KitReview.objects.order_by('-submitted_on')[:5]
    context_object_name = 'reviews'
    template_name = 'kitreviews/base.html'


class ReviewPropertyRatingInline(InlineFormSet):
    model = KitReviewPropertyRating
    form_class = modelform_factory(
        model, form=AlwaysChangedModelForm,
        fields=('id', 'prop', 'rating')
    )

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

    def get_context_data(self, **kwargs):
        print('kw', kwargs)


class FindKit(FormView):
    template_name = 'kitreviews/find_kit.html'
    form_class = FindModelKitForm

    def get_form_kwargs(self):
        kwargs = super(FindKit, self).get_form_kwargs()
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
        return self.render_to_response(self.get_context_data(kits=kits))


class KitReviewDetail(DetailView):
    model = KitReview
    template_name = 'kitreviews/kitreview_detail.html'
    context_object_name = 'kit_review'

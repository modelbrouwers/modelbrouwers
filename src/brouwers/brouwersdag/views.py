from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (DeleteView, ListView, CreateView, UpdateView,
                                  RedirectView)

from brouwers.utils.views import LoginRequiredMixin, StaffRequiredMixin
from brouwers.utils.pdf import PDFTemplateView
from .forms import ShowCasedModelSignUpForm
from .models import Brouwersdag, ShowCasedModel, Competition


class OwnModelsMixin(object):
    def get_queryset(self):
        qs = super(OwnModelsMixin, self).get_queryset()
        user = self.request.user
        return qs.filter(Q(owner=user) | Q(email=user.email)).order_by('-id')


class IndexView(ListView):
    template_name = 'brouwersdag/index.html'

    def get_queryset(self):
        current_bd = Brouwersdag.objects.get_current()
        return ShowCasedModel.objects.filter(brouwersdag=current_bd).order_by('?')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        stats = self.get_queryset().aggregate(
                n_total=Count('id'),
                n_competition=Count('competition')
            )
        context.update(stats)
        return context


class CompetitionMixin(object):
    def get_competition(self):
        if not hasattr(self, '_competition'):
            try:
                self._competition = Competition.objects.get(is_current=True)
            except Competition.DoesNotExist:  # no competition active
                self._competition = None
        return self._competition

    def get_form_kwargs(self):
        kwargs = super(CompetitionMixin, self).get_form_kwargs()
        kwargs['competition'] = self.get_competition()
        return kwargs

    def get_success_url(self):
        if self.form.cleaned_data['add_another']:
            return reverse('brouwersdag:model-signup')
        return reverse('brouwersdag:index')


class SignupView(CompetitionMixin, CreateView):
    """ View to enlist models """
    model = ShowCasedModel
    template_name = 'brouwersdag/model_signup.html'
    form_class = ShowCasedModelSignUpForm

    def get_initial(self):
        initial = super(SignupView, self).get_initial()
        if self.request.user.is_authenticated():
            initial.update({
                'owner': self.request.user.id,
                'owner_name': self.request.user.get_full_name(),
                'email': self.request.user.email,
            })
        return initial

    def form_valid(self, form):
        self.form = form
        messages.success(self.request, _('Your model has been submitted'))
        return super(SignupView, self).form_valid(form)


class EditModelView(CompetitionMixin, UpdateView):
    model = ShowCasedModel
    template_name = 'brouwersdag/model_signup_edit.html'
    form_class = ShowCasedModelSignUpForm

    def form_valid(self, form):
        self.form = form
        messages.success(self.request, _('Your model has been edited'))
        return super(EditModelView, self).form_valid(form)


class MyModelsView(LoginRequiredMixin, OwnModelsMixin, ListView):
    model = ShowCasedModel
    template_name = 'brouwersdag/my_models.html'

    def get_queryset(self):
        return super(MyModelsView, self).get_queryset().order_by('-id')


class CancelSignupView(OwnModelsMixin, DeleteView):
    model = ShowCasedModel
    success_url = reverse_lazy('brouwersdag:my-models')


class PrintSignupsView(StaffRequiredMixin, PDFTemplateView):
    template_name = 'brouwersdag/print.html'

    def get_context_data(self, **kwargs):
        kwargs['regular'] = ShowCasedModel.objects.exclude(is_competitor=True).order_by('id')
        kwargs['competition'] = ShowCasedModel.objects.filter(is_competitor=True).order_by('id')
        return super(PrintSignupsView, self).get_context_data(**kwargs)


class GoToBuildReportView(RedirectView):
    def get_redirect_url(self, **kwargs):
        q = Q(is_competitor=False) & ~Q(topic='')
        model = get_object_or_404(ShowCasedModel, q, pk=self.kwargs.get('pk'))
        return model.topic

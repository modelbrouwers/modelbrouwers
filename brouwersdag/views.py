from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import ShowCasedModelSignUpForm
from .models import ShowCasedModel, Competition


class IndexView(TemplateView):
    template_name = 'brouwersdag/index.html'


class SignupView(CreateView):
    """ View to enlist models """
    model = ShowCasedModel
    template_name = 'brouwersdag/model_signup.html'
    form_class = ShowCasedModelSignUpForm

    def get_competition(self):
        if not hasattr(self, '_competition'):
            try:
                self._competition = Competition.objects.get(is_current=True)
            except Competition.DoesNotExist: # no competition active
                self._competition = None
        return self._competition

    def get_initial(self):
        initial = super(SignupView, self).get_initial()
        if self.request.user.is_authenticated():
            initial.update({
                'owner': self.request.user.id,
                'owner_name': self.request.user.get_full_name(),
                'email': self.request.user.email,
            })
        return initial

    def get_form_kwargs(self):
        kwargs = super(SignupView, self).get_form_kwargs()
        kwargs['competition'] = self.get_competition()
        return kwargs

    def get_success_url(self):
        if self.form.cleaned_data['add_another']:
            return reverse('brouwersdag:model-signup')
        return reverse('brouwersdag:index')

    def form_valid(self, form):
        self.form = form
        messages.success(self.request, _('Your model has been submitted'))
        return super(SignupView, self).form_valid(form)

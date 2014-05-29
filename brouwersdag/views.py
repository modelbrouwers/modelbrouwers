from django.views.generic.edit import CreateView

from .forms import ShowCasedModelSignUpForm
from .models import ShowCasedModel, Competition


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

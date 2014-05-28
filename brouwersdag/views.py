from django.views.generic.edit import CreateView

from .models import ShowCasedModel


class SignupView(CreateView):
    """ View to enlist models """
    model = ShowCasedModel
    template_name = 'brouwersdag/model_signup.html'

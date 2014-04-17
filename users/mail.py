from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36

from general.mail import MultiAlternativesEmail
from .tokens import activation_token_generator


class UserRegistrationEmail(MultiAlternativesEmail):
    pass # TODO


class UserCreatedFromForumEmail(MultiAlternativesEmail):
    """ E-mail to send when an user is created from an existing forum-user """
    template_name = 'users/mail/user_created'
    subject = _('{domain} account creation - activation required')

    def __init__(self, to=None, **kwargs):
        self.user = kwargs['user']
        super(UserCreatedFromForumEmail, self).__init__(to=self.user.email, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'uidb36': int_to_base36(self.user.id),
            'token': activation_token_generator.make_token(self.user),
            'protocol': 'http'
        }
        kwargs.update(**context)
        return super(UserCreatedFromForumEmail, self).get_context_data(**kwargs)

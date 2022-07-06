from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from brouwers.general.mail import MultiAlternativesEmail


class UserRegistrationEmail(MultiAlternativesEmail):
    template_name = "users/mail/user_registered"
    subject = _("Your registration on {domain}")

    def __init__(self, to=None, **kwargs):
        self.user = kwargs.get("user")
        super().__init__(to=self.user.email, **kwargs)

    def get_subject(self):
        domain = Site.objects.get_current().domain
        return self.subject.format(domain=domain.title())

    def get_context_data(self, **kwargs):
        context = {"user": self.user}
        kwargs.update(context)
        return super().get_context_data(**kwargs)

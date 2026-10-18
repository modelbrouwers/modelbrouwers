from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from brouwers.general.mail import MultiAlternativesEmail

from .models import User


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


class RegistrationProcessedMail(MultiAlternativesEmail):
    template_name = "users/mail/registration_update"

    def __init__(self, user: User, **kwargs):
        assert user.approved_or_rejected_on is not None
        self.user = user
        super().__init__(to=user.email, **kwargs)

    def get_subject(self):
        domain = Site.objects.get_current().domain
        if self.user.is_active:
            return _("Account activated on {domain}").format(domain=domain.title())
        else:
            return _("Registration not approved")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "user": self.user,
            "is_approved": self.user.is_active,
        }

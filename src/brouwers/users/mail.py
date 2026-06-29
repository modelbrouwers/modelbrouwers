from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from brouwers.general.mail import MultiAlternativesEmail

from .models import User


class UserRegistrationEmail(MultiAlternativesEmail):
    template_name = "users/mail/user_registered"
    subject = _("Your registration on {domain}")

    user: User

    def __init__(self, user: User, to=None, **kwargs):
        self.user = user
        super().__init__(to=self.user.email, **kwargs)

    def get_subject(self):
        domain = Site.objects.get_current().domain
        return self.subject.format(domain=domain.title())

    def get_context_data(self, **kwargs):
        status_notice = (
            _("Your account has been activated - you can start using it immediately.")
            if self.user.is_active
            else _(
                "Your account was created, but must be approved by an administrator "
                "before you can use it."
            )
        )
        kwargs.update(
            {
                "user": self.user,
                "status_notice": status_notice,
            }
        )
        return super().get_context_data(**kwargs)

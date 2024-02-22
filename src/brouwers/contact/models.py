from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    name = models.CharField(_("name"), max_length=200)
    email = models.EmailField(_("email"))
    message = models.TextField(
        _("message"),
        validators=[MinLengthValidator(10), MaxLengthValidator(3000)],
        max_length=3000,
    )
    is_read = models.BooleanField(
        _("is read"),
        default=False,
        help_text=_(
            "Mark messages as read to keep track of what still requires action."
        ),
    )
    created = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("contact message")
        verbose_name_plural = _("contact messages")

    @property
    def preview(self) -> str:
        return Truncator(self.message).chars(50)

    def __str__(self):
        return _("{name} - {preview}").format(name=self.name, preview=self.preview)

    def notify_creation(self) -> None:
        """
        Send a notification email.
        """
        ...  # TODO

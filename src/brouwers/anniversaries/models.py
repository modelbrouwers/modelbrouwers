from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class RemarkableEvent(models.Model):
    date = models.DateField(
        _("date"),
        help_text=_("The day on which this significant event happened."),
    )
    title = models.CharField(
        _("title"),
        max_length=200,
        help_text=_("Short title that should invite the user to read more."),
    )
    body_text = RichTextField(
        _("body text"),
        blank=True,
        help_text=_("The full text providing more context about this specific moment."),
    )
    image = models.ImageField(
        _("image"),
        upload_to="anniversary/20/",
        blank=True,
        help_text=_("An image to display on the timeline."),
    )
    image_alt_text = models.TextField(
        _("image alt text"),
        blank=True,
        help_text=_(
            "Describe what's visible in the image for users with visual impairments. "
            "An alt text is required if you upload an image."
        ),
    )

    class Meta:
        verbose_name = _("remarkable event")
        verbose_name_plural = _("remarkable events")
        ordering = ("date",)

    def __str__(self) -> str:
        return self.title

    def clean(self):
        super().clean()

        if self.image and not self.image_alt_text:
            raise ValidationError(
                _(
                    "You must provide an alt text when adding an image to ensure "
                    "accessibilty."
                )
            )

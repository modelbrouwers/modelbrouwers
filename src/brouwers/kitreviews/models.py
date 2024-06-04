from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from brouwers.albums.models import Album
from brouwers.forum_tools.fields import ForumToolsIDField
from brouwers.kits.fields import KitForeignKey

from .constants import VoteTypes
from .managers import KitReviewQuerySet

DEFAULT_RATING = 50
MAX_RATING = 100
MIN_RATING = 0


class KitReview(models.Model):
    """
    Model holding the review information for a model kit
    """

    legacy_id = models.IntegerField(blank=True, null=True, db_index=True)
    model_kit = KitForeignKey(on_delete=models.CASCADE, verbose_name=_("model kit"))
    raw_text = models.TextField(
        _("review"),
        help_text=_("The content of the review. Please be detailed!"),
    )
    properties = models.ManyToManyField(
        "KitReviewProperty",
        blank=True,
        through="KitReviewPropertyRating",
        related_name="+",
    )

    # linking to extra information
    album = models.ForeignKey(
        Album, verbose_name=_("album"), blank=True, null=True, on_delete=models.SET_NULL
    )
    topic = ForumToolsIDField(
        _("topic"),
        type="topic",
        blank=True,
        null=True,
        help_text=_("ID of the topic on Modelbrouwers."),
    )
    external_topic_url = models.URLField(
        _("external topic url"),
        blank=True,
        help_text=_("URL to the topic not hosted on Modelbrouwers"),
    )

    # some privacy settings...
    show_real_name = models.BooleanField(
        _("show real name?"),
        default=True,
        help_text=_(
            "Checking this option will display your real name as reviewer. Uncheck to use your nickname."
        ),
    )

    # internal information
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)

    is_reviewed = models.BooleanField(_("is reviewed?"), default=False)

    objects = KitReviewQuerySet.as_manager()

    class Meta:
        verbose_name = _("kit review")
        verbose_name_plural = _("kit reviews")

    def __str__(self):
        return _("Review: %(kit)s by %(user)s") % {
            "kit": self.model_kit.name,
            "user": self.reviewer.username,
        }

    def get_absolute_url(self):
        return reverse(
            "kitreviews:review-detail",
            kwargs={"pk": self.pk, "slug": self.model_kit.slug},
        )

    @property
    def topic_url(self):
        if self.topic_id and self.topic:
            return self.topic.get_absolute_url()
        if self.external_topic_url:
            return self.external_topic_url
        return None

    @property
    def reviewer_name(self):
        if self.show_real_name:
            return self.reviewer.get_full_name()
        return self.reviewer.username


class KitReviewVote(models.Model):
    """
    Model holding the votes for kit reviews, showing the quality of the review
    """

    kit_review = models.ForeignKey(KitReview, on_delete=models.CASCADE)
    vote = models.CharField(
        _("vote"), max_length=1, db_index=True, choices=VoteTypes.choices
    )
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("kit review vote")
        verbose_name_plural = _("kit review votes")
        unique_together = (("kit_review", "voter"),)

    def __str__(self):
        return _("Vote for review by %(review_submitter)s") % {
            "review_submitter": self.kit_review.reviewer.username
        }


class KitReviewProperty(models.Model):
    """
    Model containing the possible rating properties for a review
    """

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _("kit review property")
        verbose_name_plural = _("kit review properties")

    def __str__(self):
        return self.name


class KitReviewPropertyRating(models.Model):
    """
    Represents properties for a kit review rated on a scale from MIN_RATING to MAX_RATING
    """

    kit_review = models.ForeignKey(
        "KitReview", related_name="ratings", on_delete=models.CASCADE
    )
    prop = models.ForeignKey("KitReviewProperty", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        _("rating"),
        default=DEFAULT_RATING,
        validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)],
    )

    class Meta:
        verbose_name = _("kit review property rating")
        verbose_name_plural = _("kit review property ratings")

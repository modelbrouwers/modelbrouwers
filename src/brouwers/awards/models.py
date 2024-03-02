from datetime import date

from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS, ObjectDoesNotExist, ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField

from brouwers.forum_tools.fields import ForumToolsIDField

from .constants import FIELD_2_POINTS


class Category(models.Model):
    name = models.CharField(_("name"), max_length=100)
    slug = AutoSlugField(_("slug"), populate_from="name", unique=True)
    forum = ForumToolsIDField(
        _("forum"),
        type="forum",
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def get_absolute_url(self):
        return reverse("nominations-list", kwargs={"slug": self.slug})

    def latest(self):
        """
        Returns latest five nominations in this category

        TODO: optimize with DB functions
        """
        year = date.today().year
        start_date = date(year, 1, 1)
        projects = (
            self.project_set.exclude(rejected=True)
            .filter(nomination_date__gte=start_date)
            .order_by("-nomination_date", "-id")[:5]
        )
        return projects

    def num_nominations(self):
        # TODO: optimize with DB functions
        year = date.today().year
        start_date = date(year, 1, 1)
        return (
            self.project_set.exclude(rejected=True)
            .filter(nomination_date__gte=start_date)
            .count()
        )


class LatestNominationsManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        this_year = date.today().year
        q = models.Q(nomination_date__year=this_year - 1)
        q |= models.Q(nomination_date__year=this_year)
        return qs.filter(q).exclude(rejected=True).order_by("-pk")


class Project(models.Model):
    topic = ForumToolsIDField(
        _("build report topic"),
        type="topic",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category, verbose_name="categorie", on_delete=models.CASCADE
    )

    # internal statistics
    nomination_date = models.DateField(default=date.today, db_index=True)
    votes = models.IntegerField(null=True, blank=True, default=0)
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="nominations", on_delete=models.CASCADE
    )

    last_reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        verbose_name=_("last reviewer"),
        on_delete=models.SET_NULL,
    )
    last_review = models.DateTimeField(
        _("last review"), auto_now=True, blank=True, null=True
    )

    name = models.CharField("titel verslag", max_length=100)
    brouwer = models.CharField(
        max_length=30
    )  # this should be able to be linked to an (existing) user

    image = models.ImageField(upload_to="awards/", blank=True, null=True)

    rejected = models.BooleanField(default=False)

    objects = models.Manager()
    latest = LatestNominationsManager()

    def __str__(self):
        return self.name + " - " + self.brouwer

    class Meta:
        verbose_name = _("nomination")
        verbose_name_plural = _("nominations")
        ordering = ["category", "votes"]
        unique_together = (("category", "topic"),)

    def save(self, *args, **kwargs):
        if not self.id:
            self.year = self.nomination_date.year
        super().save(*args, **kwargs)

    def sync_votes(self):
        """
        Resync the points based on the votes brought out in the following year.

        Nominated in year 20xy means votes are cast in year 20xz, where z = y +1.
        """
        year = self.nomination_date.year + 1
        base_qs = Vote.objects.filter(submitted__year=year)

        self.votes = 0
        for field, _points in FIELD_2_POINTS.items():
            f = {field: self}
            self.votes += base_qs.filter(**f).count() * _points
        self.save()


Nomination = Project


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    project1 = models.ForeignKey(Project, related_name="+", on_delete=models.CASCADE)
    project2 = models.ForeignKey(
        Project, related_name="+", blank=True, null=True, on_delete=models.SET_NULL
    )
    project3 = models.ForeignKey(
        Project, related_name="+", blank=True, null=True, on_delete=models.SET_NULL
    )

    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _("Vote by %(user)s in %(category)s") % {
            "user": self.user.username,
            "category": self.category.name,
        }

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude=exclude)

        # validate that a user can't cast multiple votes in the same year and category
        user, category, year = self.user, self.category, date.today().year
        if (
            Vote.objects.filter(user=user, category=category, submitted__year=year)
            .exclude(id=self.id)
            .exists()
        ):
            error = _(
                "User `%(user)s` already voted for `%(category)s` in `%(year)d`"
            ) % {"user": user.username, "category": category.name, "year": year}
            errors = {NON_FIELD_ERRORS: [error]}
            raise ValidationError(errors)

    def clean(self):
        _projects = list()
        for field in ("project1", "project2", "project3"):
            try:
                project = getattr(self, field, None)
                if not project:
                    continue
            except ObjectDoesNotExist:
                continue

            _projects.append(project)

            if project.category != self.category:
                raise ValidationError(
                    _(
                        "A project from `%(project_category)s` can't be voted in `%(category)s`"
                    )
                    % {
                        "project_category": project.category.name,
                        "category": self.category.name,
                    }
                )

        # validate that the projects are different
        # TODO: unittest
        if len(_projects) > len(set(_projects)):
            raise ValidationError(_("No duplicate projects are allowed"))

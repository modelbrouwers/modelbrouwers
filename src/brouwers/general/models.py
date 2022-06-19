from datetime import date, timedelta

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import get_language, ugettext_lazy as _, ungettext as _n

from brouwers.awards.models import Category

from .fields import CountryField
from .utils import get_client_ip, lookup_http_blacklist

MAX_REGISTRATION_ATTEMPTS = 3
STANDARD_BAN_TIME_HOURS = 12


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # awardsinfo
    last_vote = models.DateField(default=date(2010, 1, 1))
    forum_nickname = models.CharField(max_length=30, unique=True)
    exclude_from_nomination = models.BooleanField(
        _("exclude me from nominations"),
        help_text=_("If checked, you will be excluded from Awards-nominations."),
        default=False,
    )
    categories_voted = models.ManyToManyField(Category, blank=True)

    # address
    street = models.CharField(_("street name"), max_length=255, blank=True, null=True)
    number = models.CharField(
        _("number"),
        max_length=10,
        help_text=_("house number (+ PO box if applicable)"),
        blank=True,
    )
    postal = models.CharField(_("postal code"), max_length=10, blank=True)
    city = models.CharField(_("city"), max_length=255, blank=True)
    province = models.CharField(_("province"), max_length=255, blank=True)
    country = CountryField(blank=True)

    # allow social sharing
    allow_sharing = models.BooleanField(
        _("allow social sharing"),
        default=False,
        help_text=_(
            "Checking this gives us permission to share your topics and albums on social media. "
            "Uncheck if you don't want to share."
        ),
    )

    def __str__(self):
        return self.forum_nickname

    def full_name(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("userprofile")
        verbose_name_plural = _("userprofiles")
        ordering = ["forum_nickname"]

    @property
    def is_address_ok(self):
        ok = False
        if self.street and self.number and self.postal and self.city and self.country:
            ok = True
        return ok


class QuestionAnswer(models.Model):
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.answer


class ActiveQuestionsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_use=True)


class RegistrationQuestion(models.Model):
    question = models.CharField(
        _("Anti-spambot question"),
        max_length=255,
        help_text=_("Question which must be answered for registration."),
    )
    answers = models.ManyToManyField(QuestionAnswer, blank=True)
    in_use = models.BooleanField(default=True)

    lang = models.CharField(
        _("language"), max_length=10, choices=settings.LANGUAGES, default="nl"
    )

    objects = models.Manager()
    active = ActiveQuestionsManager()

    def __str__(self):
        return self.question


class RegistrationAttemptManager(models.Manager):
    def create_from_form(self, request, form_data):
        ip = get_client_ip(request)  # FIXME: clean format?
        kwargs = {
            "username": form_data.get("username")
            or request.POST.get("username")
            or "__blank",
            "question": form_data["question"],
            "answer": form_data.get("answer") or request.POST.get("answer"),
            "ip_address": ip,
            "email": form_data.get("email") or "",
        }

        type_of_visitor, potential_spammer = lookup_http_blacklist(ip)
        if type_of_visitor is not None and potential_spammer is not None:
            kwargs.update(
                {
                    "potential_spammer": potential_spammer,
                    "type_of_visitor": type_of_visitor,
                }
            )

        return self.create(**kwargs)


class RegistrationAttempt(models.Model):
    # same as forum_nickname
    username = models.CharField(
        _("username"), max_length=512, db_index=True, default="_not_filled_in_"
    )
    email = models.EmailField(_("email"), max_length=255, blank=True)
    question = models.ForeignKey(
        RegistrationQuestion,
        verbose_name=_("registration question"),
        on_delete=models.CASCADE,
    )
    answer = models.CharField(_("answer"), max_length=255, blank=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_("IP address"), db_index=True)
    success = models.BooleanField(_("success"), default=False)

    # keeping spam out
    potential_spammer = False
    type_of_visitor = models.CharField(
        _("type of visitor"), max_length=255, default="normal user"
    )
    ban = models.OneToOneField(
        "banning.Ban", blank=True, null=True, on_delete=models.SET_NULL
    )

    objects = RegistrationAttemptManager()

    class Meta:
        verbose_name = _("registration attempt")
        verbose_name_plural = _("registration attempts")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.username

    @property
    def question_short(self):
        return str(self.question)[:15]

    def _is_banned(self):
        return self.ban_id is not None

    _is_banned.boolean = True
    is_banned = property(_is_banned)

    def set_ban(self):
        """
        Logic to set a ban on failed registration attempts. If a ban is required,
        the time (in weeks) is exponentially in function of faulty attempts.

        Returns False if no bans were set.
        """

        num_attempts = RegistrationAttempt.objects.filter(
            ip_address=self.ip_address, success=False
        ).count()

        if num_attempts >= 2:
            from brouwers.banning.models import Ban

            kwargs = {}

            # expiry date
            if num_attempts >= MAX_REGISTRATION_ATTEMPTS:
                import math

                i = num_attempts - MAX_REGISTRATION_ATTEMPTS
                num_weeks = round(math.exp(i))
                if num_weeks <= 52:
                    kwargs["expiry_date"] = timezone.now() + timedelta(weeks=num_weeks)
                # else kwarg not set -> permaban
            else:
                kwargs["expiry_date"] = timezone.now() + timedelta(
                    hours=STANDARD_BAN_TIME_HOURS
                )

            kwargs["reason"] = _n(
                "The system flagged you as a bot or your registration attempt was not valid.",
                "You tried registering %(times)s times without succes, the system flagged you as a "
                "bot.",
                num_attempts,
            ) % {"times": num_attempts}
            kwargs["reason_internal"] = _(
                "Probably spambot, %(num_attempts)s against maximum attempts of %(max)s"
            ) % {"num_attempts": num_attempts, "max": MAX_REGISTRATION_ATTEMPTS}
            kwargs["automatic"] = True

            ban = Ban.objects.create(ip=self.ip_address, **kwargs)

            # set the ban to the registration attempt
            self.ban = ban
            self.save()
            return ban
        return False


class AnnouncementManager(models.Manager):
    def get_current(self):
        now = timezone.now()
        lang_code = get_language()[:2]
        q = Q(to_date__lt=now) | Q(from_date__gt=now)
        qs = super().get_queryset().filter(language=lang_code).exclude(q)
        if qs.exists():
            return qs[0]
        return None


class Announcement(models.Model):
    text = models.TextField()
    language = models.CharField(
        _("language"), max_length=10, choices=settings.LANGUAGES
    )
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)

    objects = AnnouncementManager()

    class Meta:
        verbose_name = _("announcement")
        verbose_name_plural = _("announcements")
        ordering = ["-from_date"]

    def __str__(self):
        return strip_tags(self.text[:50])

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from utils import do_lottery_mailing


class SecretSanta(models.Model):
    year = models.PositiveSmallIntegerField(_("year"), unique=True, help_text=_("Year the lottery starts."))
    enrollment_start = models.DateTimeField(_("enrollment start"), help_text=_("From when can people enroll."))
    enrollment_end = models.DateTimeField(_("enrollment end"), help_text=_("Until when can people enroll."))
    lottery_date = models.DateTimeField(_("lottery date"), help_text=_("When will the lottery happen?"))
    lottery_done = models.BooleanField(_("Lottery done?"), default=False)
    price_class = models.PositiveSmallIntegerField(
            _("price class"),
            blank = True, null = True,
            help_text = _("Enter a value here for the estimated price class of the gift.")
        )

    class Meta:
        verbose_name = _("secret santa")
        verbose_name_plural = _("secret santas")
        ordering = ['-year']

    def __unicode__(self):
        return u"Secret Santa %s" % self.year

    def get_price_class(self):
        price_class = self.price_class or 15
        return price_class

    #wrapper around util function
    def do_mailing(self):
        couples = self.couple_set.all().select_related('participant__user')
        do_lottery_mailing(couples)
        return None

    def is_participant(self, user):
        if user.is_authenticated():
	        p = self.participant_set.filter(user=user)
	        if p:
	            return True
        return False

    @property
    def enrollment_open(self):
        now = timezone.now()
        if self.enrollment_start <= now <= self.enrollment_end:
            return True
        return False

class Participant(models.Model):
    secret_santa = models.ForeignKey(SecretSanta, verbose_name=_("secret santa edition"), null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))

    class Meta:
        verbose_name = _("participant")
        verbose_name_plural = _("participants")
        ordering = ['secret_santa', 'user__username']

    @property
    def year(self):
        return self.secret_santa.year

    def __unicode__(self):
        return self.user.username

class Couple(models.Model):
    secret_santa = models.ForeignKey(SecretSanta, verbose_name=_("secret santa edition"), null=True)
    sender = models.ForeignKey(Participant)
    receiver = models.ForeignKey(Participant, related_name='receiver')

    def __unicode__(self):
        return u"%s - %s" % (self.sender.__unicode__(), self.receiver.__unicode__())

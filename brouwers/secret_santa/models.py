from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

class SecretSanta(models.Model):
    year = models.PositiveSmallIntegerField(_("year"), unique=True, help_text=_("Year the lottery starts."))
    enrollment_start = models.DateTimeField(_("enrollment start"), help_text=_("From when can people enroll."))
    enrollment_end = models.DateTimeField(_("enrollment end"), help_text=_("Until when can people enroll."))
    lottery_date = models.DateTimeField(_("lottery date"), help_text=_("When will the lottery happen?"))
    lottery_done = models.BooleanField(_("Lottery done?"))
    price_class = models.PositiveSmallIntegerField(
            _("price class"), 
            blank = True, null = True, 
            help_text = _("Enter a value here for the estimated price class of the gif.")
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

class Participant(models.Model):
    secret_santa = models.ForeignKey(SecretSanta, verbose_name=_("secret santa edition"), null=True)
    user = models.ForeignKey(User, verbose_name=_("user"))
    year = models.CharField(max_length=4) #TODO: deprecated
    verified = models.BooleanField() #TODO: deprecated
    
    class Meta:
        verbose_name = _("participant")
        verbose_name_plural = _("participants")
        ordering = ['secret_santa', 'user__username']
    
    def __unicode__(self):
        return u"%s" % self.user.get_profile().forum_nickname

class Couple(models.Model):
    secret_santa = models.ForeignKey(SecretSanta, verbose_name=_("secret santa edition"), null=True)
    sender = models.ForeignKey(Participant)
    receiver = models.ForeignKey(Participant, related_name='receiver')
    
    def __unicode__(self):
        return u"%s - %s" % (self.sender.__unicode__(), self.receiver.__unicode__())

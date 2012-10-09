from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from datetime import date, datetime

from brouwers.awards.models import Category

COUNTRY_CHOICES = (
	("N",_("Nederland")),
	("B",_("Belgium")),
	("D",_("Duitsland")),
	("F",_("Frankrijk")),
)

class OrderedUser(User):
    class Meta:
        ordering = ["username"]
        proxy = True
    
    def __unicode__(self):
        return u"%s" % self.username.replace('_', ' ')

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)	
	last_vote = models.DateField(default=date(2010,1,1))
	
	forum_nickname = models.CharField(max_length=30, unique=True)
	exclude_from_nomination = models.BooleanField()
	
	#awardsinfo
	secret_santa = models.BooleanField(help_text=_("Aanvinken als je meedoet"))
	categories_voted = models.ManyToManyField(Category, blank=True, null=True)
	#adres
	street = models.CharField(max_length=255, help_text=_("Straatnaam"), blank=True, null=True)
	number = models.CharField(max_length=10, help_text=_("Huisnummer (+ bus indien van toepassing)"), blank=True, null=True)
	postal = models.CharField(max_length=10, help_text=_("Postcode"), blank=True, null=True)
	city = models.CharField(max_length=255, help_text=_("Stad"), blank=True, null=True)
	province = models.CharField(max_length=255, help_text=_("Provincie"), blank=True, null=True)
	country = models.CharField(max_length=1, help_text=_("Land"),choices=COUNTRY_CHOICES, blank=True, null=True)
	
	#voorkeuren
	preference = models.TextField(help_text=_("Dit wil ik graag"), blank=True, null=True)
	refuse = models.TextField(help_text=_("Dit wil ik absoluut niet"), blank=True, null=True)
	
	def __unicode__(self):
		return self.forum_nickname
	
	def full_name(self):
		return self.user.get_full_name()
	
	class Meta:
		verbose_name = _("Gebruikersprofiel")
		verbose_name_plural = _("Gebruikersprofielen")
		ordering = ['forum_nickname']

class QuestionAnswer(models.Model):
    answer = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u"%s" % self.answer
	
class RegistrationQuestion(models.Model):
    question = models.CharField(max_length=255, help_text=_("Question which must be answered for registration."))
    answers = models.ManyToManyField(QuestionAnswer, blank=True, null=True)
    in_use = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u"%s" % self.question

class SoftwareVersion(models.Model):
    VERSION_TYPES = (
        ('a', 'alpha'),
        ('b', 'beta'),
        ('v', 'vanilla')
    )
    state = models.CharField(max_length=1, choices=VERSION_TYPES, default='v')
    major = models.PositiveSmallIntegerField(default=1)
    minor = models.PositiveSmallIntegerField(default=0)
    detail = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(default=datetime.now)
    changelog = models.TextField(blank=True)
    
    class Meta:
        ordering = ('-state', '-major', '-minor')
    
    def __unicode__(self):
        prefix = ''
        if self.state != 'v':
            prefix = '%s-' % self.get_state_display()
        detail = '.' + str(self.detail) or ''
        return u"%s%s.%s%s" % (prefix, self.major, self.minor, detail)

class PasswordReset(models.Model):
    user = models.ForeignKey(User)
    h = models.CharField(_("hash"), max_length=256)
    expire = models.DateTimeField(_("expire datetime"))
    
    class Meta:
        verbose_name = _("password reset")
        verbose_name_plural = _("password resets")
        ordering = ('expire',)
        unique_together = (('user', 'h'),)
    
    def __unicode__(self):
        return _(u"Password reset for %(user)s" % {'user': self.user.get_profile().__unicode__()})

class Redirect(models.Model):
    path_from = models.CharField(
            _("path from"), 
            max_length=512, 
            help_text=_("path from where to redirect, without leading slash. \
                        E.g. '/shop/' becomse 'shop/'."),
            unique=True
            )
    path_to = models.CharField(_("redirect to"), max_length=1024,
            help_text=_("Path (relative or absolute to the docroot) or url.")
    )
   
    class Meta:
        verbose_name = _("redirect")
        verbose_name_plural = _("redirects")
        ordering = ('path_from',)
    
    def __unicode__(self):
        return u"%s" % self.path_from

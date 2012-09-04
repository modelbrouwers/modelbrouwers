from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from datetime import date

from brouwers.awards.models import Category

COUNTRY_CHOICES = (
	("N",_("Nederland")),
	("B",_("Belgium")),
	("D",_("Duitsland")),
	("F",_("Frankrijk")),
)

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)	
	last_vote = models.DateField(default=date(2010,1,1))
	
	forum_nickname = models.CharField(max_length=20, unique=True)
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
    

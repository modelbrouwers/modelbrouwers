from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from datetime import date

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
	exclude_from_nomination = models.BooleanField(default=False)
	
	#awardsinfo
	secret_santa = models.BooleanField(help_text=_("Aanvinken als je meedoet"))
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
		return self.user.username
	
	class Meta:
		verbose_name = _("Gebruikersprofiel")
		verbose_name_plural = _("Gebruikersprofielen")
	

class Project(models.Model):
	url = models.URLField(max_length=500)
	name = models.CharField(max_length=100)
	brouwer = models.CharField(max_length=30) #this should be able to be linked to an (existing) user
	category = models.ForeignKey('Category')
	
	nomination_date = models.DateField(default=date.today())
	nominator = models.ForeignKey('UserProfile', null=True)
	
	votes = models.IntegerField(null=True, blank=True, default=0)
	rejected = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.name + ' - ' + self.brouwer
	
	class Meta:
		verbose_name = _("Nominatie")
		verbose_name_plural = _("Nominaties")

class Category(models.Model):
	name = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name = _("Categorie")
		verbose_name_plural = _(u'Categorie\u00EBn')


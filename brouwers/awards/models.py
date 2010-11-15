from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from datetime import date

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)	
	last_vote = models.DateField(default=date(2010,1,1))
	
	def __unicode__(self):
		return self.user.username
	

class Project(models.Model):
	url = models.URLField(max_length=500)
	name = models.CharField(max_length=100)
	brouwer = models.CharField(max_length=30) #this should be able to be linked to an (existing) user
	category = models.ForeignKey('Category')
	
	nomination_date = models.DateField(default=date.today())
	nominator = models.ForeignKey('UserProfile', null=True)
	
	votes = models.IntegerField(null=True, blank=True, default=0)
	
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
		verbose_name_plural = u'Categorie\u00EBn'


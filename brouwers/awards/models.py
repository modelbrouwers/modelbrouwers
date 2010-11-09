from django.db import models
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
	votes = models.IntegerField(null=True, blank=True, default=0)
	
	def __unicode__(self):
		return self.name + ' - ' + self.brouwer
	

class Category(models.Model):
	name = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name


from django.db import models
from django.utils.translation import ugettext as _
from datetime import date

class Category(models.Model):
	name = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name = _("Categorie")
		verbose_name_plural = _(u'Categorie\u00EBn')
	
	def latest(self):
		'''
		returns latest five nominations in this category
		'''
		projects = self.project_set.exclude(rejected=True).order_by('-nomination_date', '-id')[:5]
		return projects

class Project(models.Model):
	url = models.URLField(max_length=500)
	name = models.CharField(max_length=100)
	brouwer = models.CharField(max_length=30) #this should be able to be linked to an (existing) user
	category = models.ForeignKey(Category)
	
	nomination_date = models.DateField(default=date.today)
	nominator = models.ForeignKey('general.UserProfile', null=True)
	
	votes = models.IntegerField(null=True, blank=True, default=0)
	rejected = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.name + ' - ' + self.brouwer
	
	class Meta:
		verbose_name = _("Nominatie")
		verbose_name_plural = _("Nominaties")
		ordering = ['category', 'votes']

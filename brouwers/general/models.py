from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from brouwers.awards.models import Project, Category

class Build(models.Model):
	user = models.ForeignKey(User)
	url = models.URLField(max_length=500)
	title = models.CharField(max_length=255)
	category = models.ForeignKey(Category, blank=True, null=True)
	scale = models.CharField(max_length=10, blank=True)
	brand = models.CharField(max_length=64, blank=True)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	#linking with the awards
	nomination = models.ForeignKey(Project, blank=True, null=True)
	#images
	img1 = models.URLField(max_length=255, blank=True)
	img2 = models.URLField(max_length=255, blank=True)
	img3 = models.URLField(max_length=255, blank=True)
	
	def __unicode__(self):
		return _("%s - %s" % (self.user.get_profile().forum_nickname, self.title))
	
	class Meta:
		verbose_name = _("brouwverslag")
		verbose_name_plural = _("brouwverslagen")
		ordering = ['user', 'category']

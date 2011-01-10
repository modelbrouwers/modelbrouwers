from django.db import models
from django.utils.translation import ugettext as _

from brouwers.awards.models import Project, Category, UserProfile

class Build(models.Model):
	profile = models.ForeignKey(UserProfile)
	url = models.URLField(max_length=500, help_text=_("link naar het verslag"))
	title = models.CharField(_("naam model"), max_length=255, help_text=_("schaal en merk kan je apart opgeven"))
	category = models.ForeignKey(Category, blank=True, null=True, verbose_name=_("categorie"))
	scale = models.CharField(_("schaal"), max_length=10, blank=True)
	brand = models.CharField(_("merk"), max_length=64, blank=True)
	start_date = models.DateField(_("startdatum"), blank=True, null=True, help_text=_("Formaat: jjjj-mm-dd"))
	end_date = models.DateField(_("einddatum"), blank=True, null=True, help_text=_("Formaat: jjjj-mm-dd"))
	#linking with the awards
	nomination = models.ForeignKey(Project, blank=True, null=True)
	#images
	img1 = models.URLField(_("Foto 1"), max_length=255, blank=True, help_text=_("geef een link naar een foto op"))
	img2 = models.URLField(_("Foto 2"), max_length=255, blank=True, help_text=_("geef een link naar een foto op"))
	img3 = models.URLField(_("Foto 3"), max_length=255, blank=True, help_text=_("geef een link naar een foto op"))
	
	def __unicode__(self):
		return _("%s - %s" % (self.profile.forum_nickname, self.title))
	
	class Meta:
		verbose_name = _("brouwverslag")
		verbose_name_plural = _("brouwverslagen")
		ordering = ['profile', 'category']

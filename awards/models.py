from datetime import date

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError, NON_FIELD_ERRORS
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from general.shortcuts import voting_enabled


POINTS_FIRST = 3
POINTS_SECOND = 2
POINTS_THIRD = 1

FIELD_2_POINTS = {
	'project1': POINTS_FIRST,
	'project2': POINTS_SECOND,
	'project3': POINTS_THIRD,
}


class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _("category")
		verbose_name_plural = _(u'categories')

	def get_absolute_url(self):
		return reverse('nominations-list', kwargs={'slug': self.slug})

	def latest(self):
		"""
		Returns latest five nominations in this category
		"""
		year = date.today().year
		start_date = date(year, 1, 1)
		projects = self.project_set.exclude(rejected=True).filter(nomination_date__gte = start_date).order_by('-nomination_date', '-id')[:5]
		return projects

	def num_nominations(self):
		year = date.today().year
		start_date = date(year, 1, 1)
		return self.project_set.exclude(rejected=True).filter(nomination_date__gte = start_date).count()


class NominationsManager(models.Manager):
	def winners(self, year=date.today().year-1):
		""" Get the set of winning projects over all categories for ``year`` """
		if voting_enabled(year+1):
			year -= 1
		qs = super(NominationsManager, self).get_query_set().filter(nomination_date__year=year)

		winners = {}
		for project in qs.order_by('category', '-votes'):
			if project.category in winners:
				if project.votes != winners[project.category][0].votes:
					continue
			winners.setdefault(project.category, []).append(project)
		shallow = [project_list for key, project_list in winners.items()]
		return [project for sublist in shallow for project in sublist]


class LatestNominationsManager(models.Manager):
	def get_query_set(self):
		qs = super(LatestNominationsManager, self).get_query_set()
		this_year = date.today().year
		q = models.Q(nomination_date__year = this_year - 1)
		q |= models.Q(nomination_date__year = this_year)
		return qs.filter(q).exclude(rejected=True).order_by('-pk')


class Project(models.Model):
	url = models.URLField(max_length=500, help_text="link naar het verslag")
	name = models.CharField("titel verslag", max_length=100)
	brouwer = models.CharField(max_length=30) #this should be able to be linked to an (existing) user
	category = models.ForeignKey(Category, verbose_name="categorie")
	#TODO: allow for an image to be shown
	#image = models.ImageField()

	nomination_date = models.DateField(default=date.today, db_index=True)
	nominator = models.ForeignKey('general.UserProfile', null=True)

	votes = models.IntegerField(null=True, blank=True, default=0)
	rejected = models.BooleanField(default=False)

	submitter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='nominations')

	last_reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name=_('last reviewer'))
	last_review = models.DateTimeField(_('last review'), auto_now=True, blank=True, null=True)

	objects = NominationsManager()
	latest = LatestNominationsManager()

	def __unicode__(self):
		return self.name + ' - ' + self.brouwer

	class Meta:
		verbose_name = _("nomination")
		verbose_name_plural = _("nominations")
		ordering = ['category', 'votes']
		unique_together = (("category", "url"),)

	def save(self, *args, **kwargs):
		if not self.id:
			self.year = self.nomination_date.year
		super(Project, self).save(*args, **kwargs)

	def sync_votes(self):
		"""
		Resync the points based on the votes brought out in the following year.

		Nominated in year 20xy means votes are cast in year 20xz, where z = y +1.
		"""
		year = self.nomination_date.year + 1
		base_qs = Vote.objects.filter(submitted__year=year)

		self.votes = 0
		for field, _points in FIELD_2_POINTS.items():
			f = {field: self}
			self.votes += (base_qs.filter(**f).count() * _points)
		self.save()

Nomination = Project


class Vote(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	category = models.ForeignKey(Category)

	project1 = models.ForeignKey(Project, related_name='+')
	project2 = models.ForeignKey(Project, related_name='+', blank=True, null=True)
	project3 = models.ForeignKey(Project, related_name='+', blank=True, null=True)

	submitted = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return _(u"Vote by %(user)s in %(category)s") % {'user': self.user.username, 'category': self.category.name}

	def validate_unique(self, exclude=None):
		super(Vote, self).validate_unique(exclude=exclude)

		# validate that a user can't cast multiple votes in the same year and category
		user, category, year = self.user, self.category, date.today().year
		if Vote.objects.filter(user=user, category=category, submitted__year=year).exclude(id=self.id).exists():
			error = _("User `%(user)s` already voted for `%(category)s` in `%(year)d`") % {
					'user': user.username,
					'category': category.name,
					'year': year
				}
			errors = {NON_FIELD_ERRORS: [error]}
			raise ValidationError(errors)

	def clean(self):
		_projects = list()
		for field in ('project1', 'project2', 'project3'):
			try:
				project = getattr(self, field, None)
				if not project:
					continue
			except ObjectDoesNotExist:
				continue

			_projects.append(project)

			if project.category != self.category:
				raise ValidationError(_("A project from `%(project_category)s` can't be voted in `%(category)s`") % {
						'project_category': project.category.name,
						'category': self.category.name
					})

		# validate that the projects are different
		# TODO: unittest
		if len(_projects) > len(set(_projects)):
			raise ValidationError(_('No duplicate projects are allowed'))

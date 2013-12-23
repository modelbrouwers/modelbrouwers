from datetime import date

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView


from general.models import UserProfile
from general.shortcuts import voting_enabled
from .models import *
from .forms import ProjectForm


class CategoryListView(ListView):
	model = Category
	template_name = 'awards/category.html'
	context_object_name = 'categories'

	def get_queryset(self):
		qs = super(CategoryListView, self).get_queryset()
		return qs.order_by('?')


class NominationView(CreateView):
	model = Project
	form_class = ProjectForm
	template_name = 'awards/nomination.html'
	success_url = reverse_lazy('add_nomination')

	def get_initial(self):
		initial = super(NominationView, self).get_initial()
		initial.update(dict(self.request.GET.items()))
		return initial

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.submitter = self.request.user
		self.object.nominator = self.request.user.get_profile()
		self.object.save()
		if self.object.rejected:
			messages.info(request, _("The builder of this project doesn't participate in the awards."
									 " Voting for this project will not be possible."))
		else:
			messages.success(self.request, _("The nomination was added."))
		return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		kwargs['last_nominations'] = Nomination.latest.all()[:15]
		kwargs['current_year'] = date.today().year
		return super(NominationView, self).get_context_data(**kwargs)


class NominationListView(ListView):
	template_name = 'awards/category_list_nominations.html'
	context_object_name = 'projects'
	category = None

	def get_category(self):
		if self.category:
			return self.category

		pk = self.kwargs.get('pk', None)
		filter_kwargs = {'pk': pk}

		if not pk:
			slug = self.kwargs.get('slug', None)
			filter_kwargs = {'slug__iexact': slug}

		self.category = get_object_or_404(Category, **filter_kwargs)

		return self.category

	def get_queryset(self):
		category = self.get_category()
		return Nomination.objects.filter(
				category__id = category.id,
				nomination_date__year = date.today().year
			).exclude(rejected=True)

	def get_context_data(self, **kwargs):
		kwargs['category'] = self.get_category()
		return super(NominationListView, self).get_context_data(**kwargs)


@login_required
def vote(request):
	data = {}
	categories = Category.objects.all()
	year = date.today().year-1
	profile = request.user.get_profile()
	if request.method=='POST':
		for cat in categories:
			try:
				project = get_object_or_404(Project, pk=request.POST[unicode(cat)])
				project.votes += 1
				project.save()
				profile.categories_voted.add(cat)
				profile.save()
			except (ValueError, KeyError):
				pass
		profile.last_vote = date.today()
		profile.save()
		return HttpResponseRedirect('/awards/vote/scores/')
	else:
		if voting_enabled():
			if profile.last_vote.year < date.today().year:
				profile.categories_voted.clear()
			if (profile.last_vote.year == date.today().year) and (categories.count() == profile.categories_voted.count()):
				return HttpResponseRedirect('/awards/vote/scores/')
			else:
				categories_voted = profile.categories_voted.all()
				categories = categories.exclude(id__in=categories_voted)
				voted = False;
				for cat in categories:
					projects = Project.objects.filter(category__exact=cat)
					projects_valid = projects.filter(nomination_date__year = year).exclude(rejected=True)
					if not projects_valid.exists():
						profile.categories_voted.add(cat)
						profile.save()
					data[cat] = projects_valid
				return render(request, 'awards/vote.html', {'data': data, 'voted': voted, 'year': year})
		else:
			status = "De editie van %s is afgelopen, er kan niet meer gestemd worden" % year
			return render(request, 'awards/vote.html', {'status': status, 'voted': True, 'year': year})

def vote_overview(request):
	data = {}
	categories = Category.objects.all()
	year = date.today().year
	for cat in categories:
		projects = Project.objects.filter(category__exact=cat)
		projects_valid = projects.filter(nomination_date__year = year)
		data[cat] = projects_valid.exclude(rejected=True)
	return render(request, 'awards/vote_listing.html', {'data': data, 'year': year})

@user_passes_test(lambda u: u.is_authenticated(), login_url='/login/')
def scores(request):
	year = date.today().year
	if request.user.get_profile().last_vote.year != year:
		return HttpResponseRedirect('/awards/vote/')
	data = []
	voters = UserProfile.objects.filter(last_vote__year = year).count()
	year = date.today().year-1
	categories = Category.objects.all()
	categories_voted = request.user.get_profile().categories_voted.all()
	categories = categories.filter(id__in=categories_voted)
	for category in categories:
		projects = Project.objects.filter(category__exact=category, nomination_date__year = year).exclude(rejected=True).order_by('-votes')
		votes_total = 0
		if projects:
			for project in projects:
				votes_total += project.votes
			data.append({'category': category, 'projects': projects[:5], 'total': votes_total})
	return render(request, 'awards/vote_scores.html', {'data': data, 'year': year, 'voters': voters})

def winners(request):
	last_year = date.today().year-1
	url = reverse('winners', kwargs={'year': last_year})
	return redirect(url)



class WinnersView(TemplateView):

	template_name = 'awards/winners.html'

	def get_context_data(self, **kwargs):
		context = super(WinnersView, self).get_context_data(**kwargs)

		this_year = date.today().year
		year = int(self.kwargs.get('year', date.today().year))
		context['year'] = year

		# get the winners per category
		if (not voting_enabled() and year < this_year) or self.request.user.is_superuser:
			context['winners_data'] = self.get_winners(year)

		# list of years
		context['years'] = Nomination.objects.exclude(
								rejected=True
							).filter(votes__gt=0).dates(
								'nomination_date', 'year'
							).reverse()
		return context

	def get_winners(self, year):
		winners_data, prev_nomination = SortedDict(), None
		nominations = Nomination.objects.filter(
					      nomination_date__year = year,
					      rejected = False
					  ).select_related(
					      'category'
					  ).order_by('category', '-votes')
		import pdb; pdb.set_trace()
		for nomination in nominations:
			category = nomination.category

			if prev_nomination and nomination.votes == prev_nomination.votes:
				winners_data[category][position].append(nomination)
			else:
				if category not in winners_data:
					position, prev_nomination = 'first', None
					winners_data[category] = SortedDict()
				else:

					if 'second' not in winners_data[category]:
						position = 'second'
					elif 'third' not in winners_data[category]:
						position = 'third'
					else:
						continue
				winners_data[category][position] = [nomination]
			prev_nomination = nomination
		return winners_data
from collections import OrderedDict
from datetime import date
from typing import Optional

from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic import RedirectView, TemplateView
from django.views.generic.list import ListView

from brouwers.utils.views import LoginRequiredMixin

from .models import Category, Project
from .utils import voting_enabled as _voting_enabled


class NominationView(LoginRequiredMixin, RedirectView):
    pattern_name = "awards:index"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        messages.info(
            request,
            _(
                "Award nominations are currently disabled while we rework this functionality!"
            ),
        )
        return response


class NominationListView(ListView):
    queryset = Project.objects.exclude(rejected=True)
    template_name = "awards/project_list.html"
    context_object_name = "projects"
    category = None

    def get(self, request, *args, **kwargs):
        self.category = self.get_category_from_url()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.category:
            qs = qs.filter(category=self.category)
        this_year = date.today().year
        return qs.filter(nomination_date__year=this_year)

    def get_category_from_url(self) -> Optional[Category]:
        slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")

        if not (slug or pk):
            return None

        qs = Category.objects.all()
        if slug:
            qs = qs.filter(slug=slug)
        else:
            qs = qs.filter(pk=pk)
        return qs.first()

    def get_context_data(self, **kwargs):
        kwargs["category"] = self.category
        return super().get_context_data(**kwargs)


class WinnersView(TemplateView):

    template_name = "awards/winners.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_year = self.kwargs.get("year", None)
        voting_enabled = _voting_enabled()

        this_year = date.today().year
        if requested_year is not None:
            year = int(requested_year)
        else:
            year = this_year - 1
            if voting_enabled:
                year -= 1

        context["year"] = year

        # get the winners per category
        if (
            not voting_enabled
            or (voting_enabled and year < this_year - 1)
            or self.request.user.is_superuser
        ):
            context["winners_data"] = self.get_winners(year)

        # list of years
        context["years"] = (
            Project.objects.exclude(rejected=True)
            .filter(votes__gt=0)
            .dates("nomination_date", "year", order="DESC")
        )
        return context

    def get_winners(self, year):
        winners_data, prev_nomination = OrderedDict(), None
        nominations = (
            Project.objects.filter(nomination_date__year=year, rejected=False)
            .select_related("category")
            .order_by("category", "-votes")
        )

        for nomination in nominations:
            category = nomination.category

            if (
                prev_nomination
                and winners_data.get(category, False)
                and nomination.votes == prev_nomination.votes
            ):
                winners_data[category][position].append(nomination)
            else:
                if category not in winners_data:
                    position, prev_nomination = "first", None
                    winners_data[category] = OrderedDict()
                else:

                    if "second" not in winners_data[category]:
                        position = "second"
                    elif "third" not in winners_data[category]:
                        position = "third"
                    else:
                        continue
                winners_data[category][position] = [nomination]
            prev_nomination = nomination
        return winners_data

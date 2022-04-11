from collections import OrderedDict
from datetime import date

from django.views.generic import TemplateView

from .models import Project
from .utils import voting_enabled as _voting_enabled


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

from itertools import groupby
from operator import attrgetter
from typing import Optional

from django.db.models import F, Window
from django.db.models.functions import DenseRank
from django.views.generic import TemplateView

from .models import Project


def get_winners(year: int):
    nominations = (
        Project.objects.filter(nomination_date__year=year, rejected=False)
        .select_related("category")
        .annotate(
            rank=Window(
                expression=DenseRank(),
                partition_by=[F("category")],
                order_by=F("votes").desc(),
            )
        )
        .order_by("category", "rank")
    )

    top_three_per_category = {}

    for category, category_projects in groupby(nominations, key=attrgetter("category")):
        top_three_per_category[category] = {1: [], 2: [], 3: []}
        for project in category_projects:
            if project.rank > 3:  # we only care about top three
                break

            top_three_per_category[category][project.rank].append(project)

    return top_three_per_category


class WinnersView(TemplateView):

    template_name = "awards/winners.html"

    def get_context_data(self, year: Optional[int] = None, **kwargs):
        context = super().get_context_data(**kwargs)

        editions = (
            Project.objects.exclude(rejected=True)
            .filter(votes__gt=0)
            .dates("nomination_date", "year", order="DESC")
        )

        # no year provided -> pick the most recent
        if year is None and editions:
            year = editions[0].year

        top_three_per_category = get_winners(year) if year else {}

        context.update(
            {
                "editions": editions,
                "year": year,
                "top_three_per_category": top_three_per_category,
            }
        )

        return context

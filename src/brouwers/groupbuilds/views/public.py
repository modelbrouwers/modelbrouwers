from datetime import timedelta, date
import calendar

from dateutil.relativedelta import relativedelta

from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .mixins import GroupBuildDetailMixin
from ..models import GroupBuild, GroupbuildStatuses as GBStatuses
from ..forms import DateForm, ParticipantForm


class GroupBuildListView(ListView):
    model = GroupBuild
    context_object_name = 'upcoming_builds'

    def get_queryset(self):
        return GroupBuild.public.filter(
            Q(end__gte=date.today()) | Q(end=None),
        ).annotate(
            n_participants=Count('participants')
        ).distinct().order_by('category', 'start')

    def get_context_data(self, **kwargs):
        now = timezone.now()

        new_concepts = self.object_list.filter(status=GBStatuses.concept).order_by('?')[:5]
        starting_soon = self.object_list.filter(
            status=GBStatuses.accepted,
            start__gte=now + timedelta(days=3),
            start__lte=now + timedelta(weeks=6)
        ).order_by('start')

        dates = []
        form = DateForm(self.request.GET)
        today = form.get_date() or now.date()
        for i in range(0, 6):
            dates.append(today + relativedelta(months=i))

        offset_today = 100 / 6.0 * today.day / calendar.monthrange(today.year, today.month)[1]

        kwargs.update({
            'statuses': GBStatuses.choices,
            'new_concepts': new_concepts,
            'starting_soon': starting_soon,
            'calendar_gbs': self.get_calendar_builds(dates),
            'dates': dates,
            'offset_today': offset_today,
        })
        return super(GroupBuildListView, self).get_context_data(**kwargs)

    def get_calendar_builds(self, dates):
        start_date = date(dates[0].year, dates[0].month, 1)
        year, month = dates[-1].year, dates[-1].month
        end_date = date(year, month, calendar.monthrange(year, month)[1])

        qs = self.object_list.filter(
            status__in=GBStatuses.date_bound_statuses,
            end__gt=start_date,
            start__lt=end_date
        ).order_by('start', '-duration', '-end')
        for gb in qs:
            gb.set_calendar_dimensions(start_date, end_date, num_months=len(dates))
        return qs


class GroupBuildDetailView(GroupBuildDetailMixin, DetailView):
    model = GroupBuild
    queryset = GroupBuild.objects.all()
    context_object_name = 'gb'

    def get_context_data(self, **kwargs):
        ctx = super(GroupBuildDetailView, self).get_context_data(**kwargs)
        if self.object.is_open:
            ctx['participate_form'] = ParticipantForm()
        return ctx

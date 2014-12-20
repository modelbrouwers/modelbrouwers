from datetime import date, timedelta

from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard.modules import DashboardModule

from .models import GroupBuild, GroupbuildStatuses


class ModerationQueue(DashboardModule):
    title = _('Groupbuilds moderation queue')
    template = 'groupbuilds/dashboard/approve_queue.html'

    def init_with_context(self, context):
        qs = GroupBuild.objects.select_related('applicant', 'category').filter(
            status=GroupbuildStatuses.submitted
        ).order_by('start')
        self.children = list(qs)

        if not len(self.children):
            self.pre_content = _('Empty queue, good job!')


class CreateForumQueue(DashboardModule):
    title = _('Groupbuilds without forum')
    template = 'groupbuilds/dashboard/without_forum.html'

    def init_with_context(self, context):
        one_month_from_now = date.today() + timedelta(days=31)

        qs = GroupBuild.objects.select_related('category').filter(
            status=GroupbuildStatuses.accepted,
            start__gte=date.today(),
            start__lte=one_month_from_now,
            forum=None
        ).order_by('start')
        self.children = list(qs)

        if not len(self.children):
            self.pre_content = _('Empty queue, good job!')

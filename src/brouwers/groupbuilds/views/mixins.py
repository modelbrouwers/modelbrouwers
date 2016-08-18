from django.db.models import Count

from ..models import GroupBuild, GroupbuildStatuses as GBStatuses


class GroupBuildDetailMixin(object):
    """
    Mixin that checks the queryset for detail-related views
    """
    queryset = GroupBuild.public.all().annotate(n_admins=Count('admins'))

    def get_queryset(self):  # TODO: unit test
        user = self.request.user
        if user.is_authenticated:  # TODO: add staff permissions
            return (user.admin_groupbuilds.all() | self.queryset).distinct()
        return super(GroupBuildDetailMixin, self).get_queryset()

    def get_context_data(self, **kwargs):
        ctx = super(GroupBuildDetailMixin, self).get_context_data(**kwargs)

        user = self.request.user
        can_edit = (
            user.is_authenticated and self.object.status != GBStatuses.submitted and
            (user.is_superuser or self.object in user.admin_groupbuilds.all())
        )
        participants = self.object.participant_set.select_related('user').order_by('id')
        ctx.update({
            'admins': self.object.admins.all(),
            'participants': participants,
            'can_edit': can_edit,
        })

        if user.is_authenticated:
            ctx['own_models'] = [p for p in participants if p.user_id == user.id]
        return ctx

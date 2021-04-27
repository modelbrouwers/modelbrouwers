from ..models import GroupBuild, GroupbuildStatuses as GBStatuses


class GroupBuildDetailMixin(object):
    """
    Mixin that checks the queryset for detail-related views
    """

    queryset = GroupBuild.public.with_admin_count()

    def get_queryset(self):  # TODO: unit test
        user = self.request.user
        qs = super().get_queryset()

        if user.is_authenticated:  # TODO: add staff permissions
            admin_qs = user.admin_groupbuilds.with_admin_count()
            qs = (admin_qs | qs).distinct()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user = self.request.user
        can_edit = (
            user.is_authenticated
            and self.object.status != GBStatuses.submitted
            and (user.is_superuser or self.object in user.admin_groupbuilds.all())
        )
        participants = self.object.participant_set.select_related("user").order_by("id")
        ctx.update(
            {
                "admins": self.object.admins.all(),
                "participants": participants,
                "can_edit": can_edit,
            }
        )

        if user.is_authenticated:
            ctx["own_models"] = [p for p in participants if p.user_id == user.id]
        return ctx

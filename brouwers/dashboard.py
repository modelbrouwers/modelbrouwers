from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

from groupbuilds.dashboard import ModerationQueue, CreateForumQueue


class CustomIndexDashboard(Dashboard):
    title = _('Control panel')
    columns = 2

    """
    Custom index dashboard for nudge-website.
    """
    def __init__(self):
        super(CustomIndexDashboard, self).__init__()

        self.children.append(modules.ModelList(
            _('User management'),
            models=(
                'users.*',
                'general.models.UserProfile',
                'django.contrib.auth.models.Group',
                'forum_tools.models.ForumUser',
                'banning.*',
                'online_users.*',
                'general.models.PasswordReset',

            ),
        ))

        self.children.append(modules.ModelList(
            _('Group builds'),
            models=(
                'groupbuilds.*',
                'forum_tools.models.ForumLinkBase',
            )
        ))

        self.children.append(modules.ModelList(
            _('Brouwersdag'),
            models=('brouwersdag.*',)
        ))

        self.children.append(modules.ModelList(
            _('Registrations'),
            models=(
                'general.models.RegistrationAttempt',
                'general.models.RegistrationQuestion',
                'general.models.QuestionAnswer',
            )
        ))

        self.children.append(modules.ModelList(
            _('Forum'),
            models=('forum_tools.*',),
            exclude=(
                'forum_tools.models.ForumLinkBase',
                'forum_tools.models.ForumUser',
            )
        ))

        self.children.append(modules.ModelList(
            _('Albums'),
            models=('albums.*',)
        ))

        self.children.append(modules.ModelList(
            _('Awards'),
            models=('awards.*',)
        ))

        self.children.append(modules.ModelList(
            _('Misc'),
            models=('Announcement', 'Redirect')
        ))

        self.children.append(modules.ModelList(
            _('Shirts'),
            models=('shirts.*',)
        ))

        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=15
        ))

        self.children.append(ModerationQueue())
        self.children.append(CreateForumQueue())


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for nudge-website.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)

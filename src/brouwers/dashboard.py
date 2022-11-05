from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import AppIndexDashboard, Dashboard, modules

from brouwers.groupbuilds.dashboard import CreateForumQueue, ModerationQueue


class CustomIndexDashboard(Dashboard):
    title = _("Control panel")
    columns = 3

    """
    Custom index dashboard for nudge-website.
    """

    def __init__(self):
        super().__init__()

        self.children.append(
            modules.ModelList(
                _("User management"),
                models=(
                    "brouwers.users.*",
                    "brouwers.general.models.UserProfile",
                    "brouwers.django.contrib.auth.models.Group",
                    "brouwers.forum_tools.models.ForumUser",
                    "brouwers.banning.*",
                    "brouwers.online_users.*",
                    "brouwers.general.models.PasswordReset",
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                _("Shop: orders"),
                models=(
                    "brouwers.shop.models.cart.Cart",
                    "brouwers.shop.models.payments.Payment",
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                _("Shop: products"),
                models=(
                    "brouwers.shop.models.categories.Category",
                    "brouwers.shop.models.categories.CategoryCarouselImage",
                    "brouwers.shop.models.products.Product",
                    "brouwers.shop.models.products.ProductImage",
                    "brouwers.shop.models.products.ProductManufacturer",
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                _("Shop: config"),
                models=(
                    "brouwers.shop.models.config.ShopConfiguration",
                    "brouwers.shop.models.payments.PaymentMethod",
                    "brouwers.shop.models.presentation.HomepageCategory",
                    "brouwers.shop.models.presentation.HomepageCategoryChild",
                    "brouwers.shop.models.customers.CustomerGroup",
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                _("Group builds"),
                models=(
                    "brouwers.groupbuilds.*",
                    "brouwers.forum_tools.models.ForumLinkBase",
                ),
            )
        )

        self.children.append(
            modules.ModelList(_("Brouwersdag"), models=("brouwers.brouwersdag.*",))
        )

        self.children.append(
            modules.ModelList(
                _("Registrations"),
                models=(
                    "brouwers.general.models.RegistrationAttempt",
                    "brouwers.general.models.RegistrationQuestion",
                    "brouwers.general.models.QuestionAnswer",
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                _("Forum"),
                models=("brouwers.forum_tools.*",),
                exclude=(
                    "brouwers.forum_tools.models.ForumLinkBase",
                    "brouwers.forum_tools.models.ForumUser",
                ),
            )
        )

        self.children.append(
            modules.ModelList(_("Albums"), models=("brouwers.albums.*",))
        )

        self.children.append(
            modules.ModelList(_("Awards"), models=("brouwers.awards.*",))
        )

        self.children.append(
            modules.ModelList(_("Misc"), models=("Announcement", "Redirect"))
        )

        self.children.append(
            modules.ModelList(_("Shirts"), models=("brouwers.shirts.*",))
        )

        self.children.append(modules.RecentActions(title=_("Recent Actions"), limit=15))

        self.children.append(ModerationQueue())
        self.children.append(CreateForumQueue())


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for nudge-website.
    """

    # we disable title because its redundant with the model list module
    title = ""

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _("Recent Actions"), include_list=self.get_app_content_types(), limit=5
            ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super().init_with_context(context)

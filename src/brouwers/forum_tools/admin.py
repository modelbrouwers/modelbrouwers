from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    BuildReportsForum,
    Forum,
    ForumCategory,
    ForumPostCountRestriction,
    ForumUser,
    Report,
)


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("__str__", "forum_name", "forum_id", "forum_desc")
    list_editable = ("forum_name",)
    search_fields = ("forum_name", "forum_desc")


@admin.register(BuildReportsForum)
class BuildReportsForumAdmin(admin.ModelAdmin):
    list_display = ("__str__", "forum")


@admin.register(ForumUser)
class ForumUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "user_email",
        "show_absolute_url",
        "user_posts",
        "user_email_hash",
        "get_email_hash",
    )
    search_fields = ("username", "user_email")

    @admin.display(description=_("Link"))
    def show_absolute_url(self, obj):
        return format_html(
            '<a href="%s">%s</a>',
            obj.get_absolute_url(),
            _("forum profile"),
        )


@admin.register(ForumPostCountRestriction)
class ForumPostCountRestrictionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "min_posts", "posting_level")
    list_editable = ("min_posts", "posting_level")
    list_filter = ("forum", "posting_level")
    search_fields = ("forum__forum_name",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("report_time", "report_closed", "report_text")
    list_filter = ("report_closed",)


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "forum", "icon_class")
    list_editable = ("forum", "icon_class")
    search_fields = ("name",)

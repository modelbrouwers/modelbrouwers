from django.contrib import admin
from django.utils.translation import ugettext

from .models import (
    BuildReportsForum, Forum, ForumCategory, ForumLinkBase, ForumLinkSynced,
    ForumPostCountRestriction, ForumUser, Report
)


class ForumLinkSyncedInline(admin.TabularInline):
    model = ForumLinkSynced


@admin.register(ForumLinkBase)
class ForumLinkBaseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'link_id', 'enabled', 'from_date', 'to_date')
    list_editable = ('link_id', 'enabled', 'from_date', 'to_date')
    list_filter = ('enabled', 'from_date', 'to_date')
    inlines = [ForumLinkSyncedInline]


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'forum_name', 'forum_id', 'forum_desc')
    list_editable = ('forum_name',)
    search_fields = ('forum_name', 'forum_desc')


@admin.register(BuildReportsForum)
class BuildReportsForumAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'forum')


@admin.register(ForumUser)
class ForumUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_email',
                    'show_absolute_url', 'user_posts',
                    'user_email_hash', 'get_email_hash')
    search_fields = ('username', 'user_email')

    def show_absolute_url(self, obj):
        click = ugettext('forum profile')
        return '<a href=\"%s\">%s</a>' % (obj.get_absolute_url(), click)
    show_absolute_url.allow_tags = True
    show_absolute_url.short_description = ugettext('Link')


@admin.register(ForumPostCountRestriction)
class ForumPostCountRestrictionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'min_posts', 'posting_level')
    list_editable = ('min_posts', 'posting_level')
    list_filter = ('forum', 'posting_level')
    search_fields = ('forum__forum_name',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_time', 'report_closed', 'report_text')
    list_filter = ('report_closed',)


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'forum', 'icon_class')
    list_editable = ('forum', 'icon_class')
    search_fields = ('name',)

from django.contrib import admin
from django.utils.translation import ugettext
from models import *


class ForumLinkSyncedInline(admin.TabularInline):
    model = ForumLinkSynced


class ForumLinkBaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'link_id', 'enabled', 'from_date', 'to_date')
    list_editable = ('link_id', 'enabled', 'from_date', 'to_date')
    list_filter = ('enabled', 'from_date', 'to_date')
    inlines = [ForumLinkSyncedInline]


class ForumAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'forum_name', 'forum_id', 'forum_desc')#, 'parent')
    list_editable = ('forum_name',) #'forum_desc')
    search_fields = ('forum_name', 'forum_desc')


class BuildReportsForumAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'forum_id')


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


class ForumPostCountRestrictionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'min_posts', 'posting_level')
    list_editable = ('min_posts', 'posting_level')
    list_filter = ('forum', 'posting_level')
    search_fields = ('forum__forum_name',)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_time', 'report_closed', 'report_text')
    list_filter = ('report_closed',)


class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'forum_id', 'icon_class')
    list_editable = ('forum_id', 'icon_class')
    search_fields = ('name',)


admin.site.register(ForumUser, ForumUserAdmin)
admin.site.register(ForumLinkBase, ForumLinkBaseAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(BuildReportsForum, BuildReportsForumAdmin)
admin.site.register(ForumPostCountRestriction, ForumPostCountRestrictionAdmin)
admin.site.register(ForumCategory, ForumCategoryAdmin)

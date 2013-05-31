from django.contrib import admin
from django.utils.translation import ugettext
from models import *

class ForumLinkBaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'link_id', 'enabled', 'from_date', 'to_date')
    list_editable = ('link_id', 'enabled', 'from_date', 'to_date')
    list_filter = ('enabled', 'from_date', 'to_date')

class ForumLinkSyncedAdmin(admin.ModelAdmin):
    list_display = ('base', 'link_id')
    list_editable = ('link_id',)
    list_filter = ('base__enabled',)

class ForumUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_email', 
                    'show_absolute_url', 'user_posts',
                    'user_email_hash', 'get_email_hash')
    search_fields = ('username',)
    
    def show_absolute_url(self, obj):
        click = ugettext('forum profile')
        return '<a href=\"%s\">%s</a>' % (obj.get_absolute_url(), click)
    show_absolute_url.allow_tags = True
    show_absolute_url.short_description = ugettext('Link')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_time', 'report_closed', 'report_text')
    list_filter = ('report_closed',)

admin.site.register(ForumUser, ForumUserAdmin)
admin.site.register(ForumLinkBase, ForumLinkBaseAdmin)
admin.site.register(ForumLinkSynced, ForumLinkSyncedAdmin)
admin.site.register(Report, ReportAdmin)

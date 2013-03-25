from django.contrib import admin
from models import *

class ForumLinkBaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'link_id', 'enabled', 'from_date', 'to_date')
    list_editable = ('link_id', 'enabled', 'from_date', 'to_date')
    list_filter = ('enabled', 'from_date', 'to_date')

class ForumLinkSyncedAdmin(admin.ModelAdmin):
    list_display = ('base', 'link_id')
    list_editable = ('link_id',)
    list_filter = ('base__enabled',)

admin.site.register(ForumLinkBase, ForumLinkBaseAdmin)
admin.site.register(ForumLinkSynced, ForumLinkSyncedAdmin)

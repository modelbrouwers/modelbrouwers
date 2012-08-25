from models import *
from django.contrib import admin

class UserMigrationAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'username', 'username_clean', 'email', 'hash')
	list_editable = ('username', 'email')
	list_display_links = ('__unicode__',)
	search_fields = ('username',)

admin.site.register(UserMigration, UserMigrationAdmin)

from models import *
from django.contrib import admin

class UserMigrationAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'username', 'username_clean', 'email', 'hash', 'url')
	list_editable = ('username', 'email')
	list_display_links = ('__unicode__',)
	search_fields = ('username',)

class AlbumUserMigrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'django_user')
    search_fields = ('username',)

admin.site.register(UserMigration, UserMigrationAdmin)
admin.site.register(AlbumUserMigration, AlbumUserMigrationAdmin)

from models import *
from django.contrib import admin

class UserMigrationAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'username', 'username_clean', 'email', 'hash', 'url')
	list_editable = ('username', 'email')
	list_display_links = ('__unicode__',)
	search_fields = ('username',)

class AlbumUserMigrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'django_user')
    search_fields = ('username',)

class AlbumMigrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'owner', 'migrated', 'new_album')
    list_editable = ('title', 'description', 'migrated')
    list_filter = ('migrated', 'owner')
    search_fields = ('owner__username', 'title', 'description')

class PictureMigrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'album', '__unicode__', 'migrated')
    list_editable = ('migrated',)
    list_filter = ('migrated',)
    search_fields = ('owner__username', 'album__owner__username', 'caption', 'title')

admin.site.register(UserMigration, UserMigrationAdmin)
admin.site.register(AlbumUserMigration, AlbumUserMigrationAdmin)
admin.site.register(AlbumMigration, AlbumMigrationAdmin)
admin.site.register(PhotoMigration, PictureMigrationAdmin)

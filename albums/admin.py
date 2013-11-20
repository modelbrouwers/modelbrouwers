from models import *
from django.contrib import admin

class AlbumAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'clean_title', 'last_upload', 'created', 'public', 'writable_to', 'order')
	list_editable = ('title', 'clean_title', 'public', 'order')
	list_filter = ('user', 'public', 'writable_to', 'created', 'trash')
	search_fields = ('title', 'description')
	raw_id_fields = ('user', 'cover')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'name', 'order',)
	list_editable = ('name', 'order',)
	search_fields = ('name',)

class PhotoAdmin(admin.ModelAdmin):
	list_display = ('user', 'album', 'views', 'uploaded', 'BBCode')
	list_filter = ('user', 'album')
	raw_id_fields = ('user', 'album')

class PreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_img_size', 'default_uploader', 'auto_start_uploading')
    list_editable = ('default_img_size', 'default_uploader', 'auto_start_uploading')
    list_filter = ('default_uploader', 'default_img_size')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)

class AlbumDownloadAdmin(admin.ModelAdmin):
    list_display = ('album', 'downloader', 'timestamp', 'failed')
    list_filter = ('timestamp', 'failed')
    search_fields = ('album__title', 'downloader__username')
    raw_id_fields = ('downloader', 'album')

class AlbumGroupAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('album__title',)
    filter_horizontal = ('users',)

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Preferences, PreferencesAdmin)
admin.site.register(AlbumDownload, AlbumDownloadAdmin)
admin.site.register(AlbumGroup, AlbumGroupAdmin)

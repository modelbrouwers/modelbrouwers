from django.contrib import admin

from .models import (
    Album, AlbumDownload, AlbumGroup, Category, Photo, Preferences
)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'clean_title', 'last_upload', 'created', 'public', 'writable_to', 'order')
    list_editable = ('title', 'clean_title', 'public', 'order')
    list_filter = ('public', 'writable_to', 'created', 'trash')
    search_fields = ('=id', 'title', 'description')
    raw_id_fields = ('user', 'cover')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'order',)
    list_editable = ('name', 'order',)
    search_fields = ('name',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'views', 'uploaded')
    list_filter = ('album', 'uploaded')
    raw_id_fields = ('user', 'album')


@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'auto_start_uploading')
    list_editable = ('auto_start_uploading',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)


@admin.register(AlbumDownload)
class AlbumDownloadAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'album', 'downloader', 'timestamp', 'failed')
    list_filter = ('timestamp', 'failed')
    search_fields = ('album__title', 'downloader__username')
    raw_id_fields = ('downloader', 'album')


@admin.register(AlbumGroup)
class AlbumGroupAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('album__title',)
    filter_horizontal = ('users',)

from models import *
from django.contrib import admin

class AlbumAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'created', 'public', 'writable_to')
	list_filter = ('user', 'public', 'writable_to', 'created')
	search_fields = ('title', 'description')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'name', 'order',)
	list_editable = ('name', 'order',)
	search_fields = ('name',)

class PhotoAdmin(admin.ModelAdmin):
	list_display = ('user', 'album', 'views', 'uploaded', 'BBCode')
	list_filter = ('user', 'album')

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category, CategoryAdmin)

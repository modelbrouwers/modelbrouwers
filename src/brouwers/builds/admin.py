from django.contrib import admin

from .models import Build, BuildPhoto


class BuildPhotoInline(admin.TabularInline):
    model = BuildPhoto
    raw_id_fields = ('photo',)


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'kit')
    raw_id_fields = ('user', 'kit')
    inlines = (BuildPhotoInline,)


@admin.register(BuildPhoto)
class BuildPhotoAdmin(admin.ModelAdmin):
    list_display = ('build', 'photo', 'photo_url', 'order')
    list_editable = ('order',)
    search_fields = ('build__slug',)
    raw_id_fields = ('photo',)

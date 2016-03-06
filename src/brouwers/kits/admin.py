from django.contrib import admin

from .models import Brand, Scale, ModelKit


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'is_active', 'slug')
    list_filter = ('is_active',)
    search_fields = ('=id', 'name')


@admin.register(Scale)
class ScaleAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('scale',)


@admin.register(ModelKit)
class ModelKitAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'scale', 'box_image')
    list_filter = ('brand', 'scale')
    search_fields = ('name', 'kit_number')
    raw_id_fields = ('submitter',)
    filter_horizontal = ('duplicates',)

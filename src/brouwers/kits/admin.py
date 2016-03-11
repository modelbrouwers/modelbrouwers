from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from django.db.models import Prefetch
from django.utils.translation import ugettext_lazy as _

from brouwers.builds.models import Build
from brouwers.utils.admin.decorators import link_list
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
    list_display = ('name', 'brand', 'scale', 'get_builds', 'get_box_image_url')
    list_filter = ('is_reviewed', 'brand', 'scale')
    search_fields = ('name', 'kit_number')
    raw_id_fields = ('submitter',)
    filter_horizontal = ('duplicates',)

    def get_queryset(self, request=None):
        prefetch = Prefetch('builds', queryset=Build.objects.select_related('user'))
        return super(ModelKitAdmin, self).get_queryset(request=request).prefetch_related(prefetch)

    @link_list(short_description=_('builds'))
    def get_builds(self, obj):
        return obj.builds.all()

    def get_box_image_url(self, obj):
        if obj.box_image:
            return '<a href="{0}" target="_blank">{1}</a>'.format(obj.box_image.url, _('view image'))
        return ''
    get_box_image_url.allow_tags = True
    get_box_image_url.short_description = _('boxart')

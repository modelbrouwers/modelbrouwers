from django.contrib import admin
from django.utils.translation import ugettext as _


from .models import *


class BuildAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'brand', 'scale')
    fieldsets = (
        (_('General information'), {
            'fields': (
                ('profile', 'user'),
                'title',
                'url',
                ('topic_id', 'forum_id'),
                )
            }
        ),
        (_('Kit information'), {
            'fields': (
                ('brand', 'scale'),
                ),
            'classes': ['collapse'],
            }
        ),
        ('Varia', {
            'fields': (
                ('start_date', 'end_date'), 
                ),
            'classes': ['collapse'],
        }),
        (None, {
            'fields': ('slug',),
            }
        )
    )
    
    prepopulated_fields = {
        'slug': ('title',),
        }

class BuildPhotoAdmin(admin.ModelAdmin):
    list_display = ('build', 'photo', 'photo_url', 'order')
    list_editable = ('order',)
    search_fields = ('build__slug',)
    raw_id_fields = ('photo',)

admin.site.register(Build, BuildAdmin)
admin.site.register(BuildPhoto, BuildPhotoAdmin)

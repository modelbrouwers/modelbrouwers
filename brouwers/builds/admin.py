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
                'brand_name',
                ),
            'classes': ['collapse'],
            }
        ),
        ('Varia', {
            'fields': (
                ('start_date', 'end_date'), 
                'img1', 
                'img2', 
                'img3'
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

admin.site.register(Build, BuildAdmin)

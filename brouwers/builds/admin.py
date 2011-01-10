from django.contrib import admin
from models import *

class BuildAdmin(admin.ModelAdmin):
	fieldsets = (
		('Forum Info', {
			'fields': ('profile', 'url', 'title', 'category')
		  }),
		('Kit Info', {
			'classes': ['collapse'],
			'fields': (('brand', 'scale'),)
		}),
		('Varia', {
			'classes': ['collapse'],
			'fields': ('nomination', 'img1', 'img2', 'img3')
		})
	)
	
	list_display = ('profile', 'title', 'brand', 'scale')

admin.site.register(Build, BuildAdmin)

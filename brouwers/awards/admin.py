from brouwers.awards.models import *
from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):
	fields = ['url', 'brouwer', 'name', 'category','nomination_date','nominator', 'rejected', 'votes']
	list_display = ('name', 'brouwer','category','nomination_date', 'nominator', 'rejected', 'votes')

class UserProfileAdmin(admin.ModelAdmin):
	fieldsets = (
		('General', {
			'fields': ('user', 'forum_nickname')
		  }),
		('Awards', {
#			'classes': ['collapse'],
			'fields': ('last_vote', 'exclude_from_nomination')
		}),
		('Secret Santa', {
#			'classes': ['collapse'],
			'fields': ('secret_santa', ('street','number'),('postal', 'city'),('province','country'), 'preference', 'refuse')
		})
	)
	
	list_display = ('forum_nickname', 'user', 'full_name', 'exclude_from_nomination', 'secret_santa')



admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(UserProfile, UserProfileAdmin)

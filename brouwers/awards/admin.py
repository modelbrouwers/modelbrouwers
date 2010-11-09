from brouwers.awards.models import *
from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):
	fields = ['url', 'brouwer', 'name', 'category','nomination_date', 'votes']
	list_display = ('name', 'brouwer','category','nomination_date', 'votes')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)

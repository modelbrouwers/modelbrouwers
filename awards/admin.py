from models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

def reject(modeladmin, request, queryset):
    queryset.update(rejected=True)
reject.short_description = "Maak nominaties ongeldig"

class ProjectAdmin(admin.ModelAdmin):
	fields = ['url', 'brouwer', 'name', 'category','nomination_date','nominator', 'rejected', 'votes']
	list_display = ('name', 'show_url', 'brouwer','category','nomination_date', 'nominator', 'rejected', 'votes')
	list_filter = ('category', 'nomination_date')
	actions = [reject]
	
	def show_url(self, obj):
		return '<a href="%s">topic</a>' % obj.url
	show_url.allow_tags = True
	show_url.short_description = 'Topic url'

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_superuser')
UserAdmin.ordering = ['-date_joined', 'username']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

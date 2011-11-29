from models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProjectAdmin(admin.ModelAdmin):
	fields = ['url', 'brouwer', 'name', 'category','nomination_date','nominator', 'rejected', 'votes']
	list_display = ('name', 'brouwer','category','nomination_date', 'nominator', 'rejected', 'votes')
	list_filter = ('category', 'nomination_date')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_superuser')
UserAdmin.ordering = ['-date_joined', 'username']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

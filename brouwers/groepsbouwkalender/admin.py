from models import *
from django.contrib import admin

class GroepsbouwAdmin(admin.ModelAdmin):
	list_display = ('applicant', 'buildname', 'forumpart', 'start_date', 'end_date', 
    'duration', 'description', 'topiclink', 'status', 'opmerkingen')
    
	list_filter = ('forumpart', 'start_date', 'end_date', 'duration', 'status')
    
	search_fields = ('buildname', 'description')

admin.site.register(Groepsbouw, GroepsbouwAdmin)
from django.contrib import admin
from brouwers.secret_santa.models import *

class ParticipantAdmin(admin.ModelAdmin):
	list_display = ('user', 'year')

admin.site.register(Participant, ParticipantAdmin)

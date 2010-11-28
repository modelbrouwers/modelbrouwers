from django.contrib import admin
from brouwers.secret_santa.models import *

class ParticipantAdmin(admin.ModelAdmin):
	list_display = ('user', 'year', 'verified')

class CoupleAdmin(admin.ModelAdmin):
	list_display = ('sender', 'receiver')

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Couple, CoupleAdmin)

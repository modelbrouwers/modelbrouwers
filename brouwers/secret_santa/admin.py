from django.contrib import admin
from brouwers.secret_santa.models import *

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'verified')
    list_editable = ('verified',)
    list_filter = ('user',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

class CoupleAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver')

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Couple, CoupleAdmin)

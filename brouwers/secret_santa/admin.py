from django.contrib import admin
from brouwers.secret_santa.models import *

class SecretSantaAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'enrollment_start', 'enrollment_end', 'lottery_date', 'lottery_done')
    list_editable = ('enrollment_start', 'enrollment_end', 'lottery_date', 'lottery_done')
    search_fields = ('year',)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'verified')
    list_editable = ('verified',)
    list_filter = ('secret_santa', 'year', 'verified')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

class CoupleAdmin(admin.ModelAdmin):
    list_display = ('secret_santa', 'sender', 'receiver')
    list_filter = ('secret_santa',)

admin.site.register(SecretSanta, SecretSantaAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Couple, CoupleAdmin)

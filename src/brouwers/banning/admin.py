from django.contrib import admin

from .models import Ban


@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip', 'expiry_date', 'automatic', 'registration_attempt')
    list_filter = ('automatic', 'expiry_date',)
    search_fields = ('user__username', 'registrationattempt__username', 'ip')

    def registration_attempt(self, obj):
        return obj.registrationattempt

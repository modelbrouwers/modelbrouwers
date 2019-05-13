from django.contrib import admin

from .models import TrackedUser


@admin.register(TrackedUser)
class TrackedUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'last_seen', 'notificate', 'is_online')
    list_editable = ('notificate',)
    list_filter = ('last_seen', 'notificate')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

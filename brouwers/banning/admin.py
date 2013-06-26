from django.contrib import admin
from models import *


class BanAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip', 'expiry_date', 'automatic')
    list_filter = ('automatic', 'expiry_date',)
    search_fields = ('user__username',)


admin.site.register(Ban, BanAdmin)
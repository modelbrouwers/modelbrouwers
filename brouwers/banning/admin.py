from django.contrib import admin
from models import *


class BanAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip', 'expiry_date')
    list_filter = ('expiry_date',)
    search_fields = ('user__username',)


admin.site.register(Ban, BanAdmin)
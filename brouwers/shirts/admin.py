from models import *
from django.contrib import admin

class ShirtOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user__email', 'size', 'type', 'color', 'moderator', 'send_per_mail', 'order_time', 'price', 'payment_received')
    list_editable = ('payment_received',)
    list_filter = ('size', 'type', 'color', 'moderator', 'send_per_mail', 'order_time', 'payment_received')

admin.site.register(ShirtOrder, ShirtOrderAdmin)

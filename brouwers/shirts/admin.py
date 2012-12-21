from models import *
from django.contrib import admin

class ShirtOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_email', 'size', 'type', 'color', 'moderator', 'send_per_mail', 'order_time', 'price', 'payment_received', 'delivered' )
    list_editable = ('payment_received', 'delivered')
    list_filter = ('size', 'type', 'color', 'moderator', 'send_per_mail', 'order_time', 'payment_received', 'delivered')

admin.site.register(ShirtOrder, ShirtOrderAdmin)

from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "preview", "created", "is_read")
    list_filter = ("is_read", "created")
    list_editable = ("is_read",)
    ordering = ("-created",)
    date_hierarchy = "created"
    search_fields = (
        "email",
        "name",
    )

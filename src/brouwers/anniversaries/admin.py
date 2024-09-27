from django.contrib import admin

from .models import RemarkableEvent


@admin.register(RemarkableEvent)
class RemarkableEventAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    list_filter = ("date",)
    date_hierarchy = "date"
    search_fields = ("title",)

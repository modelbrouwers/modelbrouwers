from django.contrib import admin

from .models import OcSetting


@admin.register(OcSetting)
class OcSettingAdmin(admin.ModelAdmin):
    list_display = ("group", "key", "store_id")
    list_filter = ("group", "store_id")
    search_fields = ("group", "key")
    ordering = ("group", "key")

    def has_add_permission(self, request) -> bool:  # pragma: no cover
        return False

    def has_change_permission(self, request, obj=None) -> bool:  # pragma: no cover
        return False

    def has_delete_permission(self, request, obj=None) -> bool:  # pragma: no cover
        return False

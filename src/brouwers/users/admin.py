from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from brouwers.general.utils import lookup_country

from .forms import AdminUserCreationForm
from .models import DataDownloadRequest, User


@admin.register(User)
class UserAdmin(_UserAdmin):
    list_display = (
        "username",
        "email",
        "date_joined",
        "is_active",
        "registration_complete",
        "location_details",
        "forumuser_id",
    )
    fieldsets = _UserAdmin.fieldsets + (  # type: ignore
        (
            _("Extra"),
            {
                "fields": (
                    "forumuser_id",
                    "ui_language",
                    "ip_address_joined",
                )
            },
        ),
        (
            _("Registration"),
            {
                "fields": (
                    "registration_motivation",
                    "approved_or_rejected_on",
                ),
            },
        ),
    )

    ordering = ("-date_joined", "username")
    add_form = AdminUserCreationForm
    change_form_template = "loginas/change_form.html"
    readonly_fields = ("registration_motivation", "approved_or_rejected_on")

    @admin.display(description=_("Registration complete"), boolean=True)
    def registration_complete(self, obj: User) -> bool:
        return not obj.needs_registration_approval

    @admin.display(description=_("location details"))
    def location_details(self, obj: User) -> str | None:
        if not (ip := obj.ip_address_joined):
            return None
        country = lookup_country(ip)
        return format_html(
            "<strong>{country}</strong><br>IP: <code>{ip}</code>",
            country=country or _("country unknown"),
            ip=ip,
        )


@admin.register(DataDownloadRequest)
class DataDownloadRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "finished")
    list_filter = ("created", "finished")
    list_select_related = ("user",)
    date_hierarchy = "created"
    search_fields = ("user__id", "user__username", "user__email")
    readonly_fields = ("zip_file",)
    raw_id_fields = ("user",)

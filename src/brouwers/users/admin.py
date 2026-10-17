from typing import override

from django.contrib import admin, messages
from django.contrib.admin.utils import unquote
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
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
        "registration_status",
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

    @override
    def get_urls(self):
        custom = [
            path(
                "<path:object_id>/approve-registration/",
                self.admin_site.admin_view(self.registration_approval),
                name="user_registration_approval",
            ),
        ]
        return custom + super().get_urls()

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

    @admin.display(description=("Registration"))
    def registration_status(self, obj: User) -> str:
        from django.contrib.admin.templatetags.admin_list import _boolean_icon

        if not obj.needs_registration_approval:
            return _boolean_icon(obj.is_active)
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:user_registration_approval", kwargs={"object_id": obj.pk}),
            _("Approve or reject"),
        )

    @transaction.atomic()
    def registration_approval(self, request: HttpRequest, object_id: str):
        user = self.get_object(request, unquote(object_id))
        assert isinstance(user, User)

        if not self.has_change_permission(request, user):
            raise PermissionDenied

        if user.approved_or_rejected_on is not None:
            self.message_user(
                request,
                _("The user registration is already processed."),
                level=messages.WARNING,
            )
            return redirect("admin:users_user_change", object_id=user.pk)

        if request.method == "POST":
            is_approved = "approve" in request.POST
            is_rejected = "reject" in request.POST
            if not is_approved and not is_rejected:
                self.message_user(
                    request, _("You must pick approve or reject."), level=messages.ERROR
                )
            else:
                user.is_active = is_approved
                user.approved_or_rejected_on = timezone.now()
                user.save()
                msg = (
                    _("The user account is now activated.")
                    if is_approved
                    else _("User registration rejected.")
                )
                self.message_user(
                    request,
                    msg,
                    level=messages.SUCCESS if is_approved else messages.INFO,
                )
                # TODO: send email with result
                return redirect("admin:users_user_changelist")

        return TemplateResponse(
            request,
            "admin/users/user/registration_approval.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Approve or reject user signup"),
                "subtitle": str(user),
                "opts": self.opts,
                "original": _("Signup of: {user}").format(user=user),
                "user": user,
                "location_details": self.location_details(user),
            },
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

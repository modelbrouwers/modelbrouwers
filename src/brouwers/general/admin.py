from django.contrib import admin

from .models import Announcement, RegistrationAttempt, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General", {"fields": ("user", "forum_nickname")}),
        (
            "Awards",
            {"fields": (("last_vote", "exclude_from_nomination"), "categories_voted")},
        ),
        (
            "Address",
            {
                "fields": (
                    ("street", "number"),
                    ("postal", "city"),
                    ("province", "country"),
                )
            },
        ),
    )

    list_display = (
        "forum_nickname",
        "user",
        "full_name",
        "exclude_from_nomination",
        "last_vote",
    )
    list_filter = ("exclude_from_nomination",)
    search_fields = ("forum_nickname", "user__email")


class RegistrationAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "timestamp",
        "ip_address",
        "success",
        "is_banned",
        "type_of_visitor",
    )
    list_filter = ("success", "timestamp", "type_of_visitor")
    search_fields = ("username",)
    actions = None


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("__str__", "from_date", "to_date")
    list_filter = ("language", "from_date", "to_date")
    list_editable = ("from_date", "to_date")
    search_fields = ("text",)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RegistrationAttempt, RegistrationAttemptAdmin)
admin.site.register(Announcement, AnnouncementAdmin)

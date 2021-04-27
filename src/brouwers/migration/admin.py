from django.contrib import admin

from .models import AlbumMigration, AlbumUserMigration, PhotoMigration, UserMigration


@admin.register(UserMigration)
class UserMigrationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "username", "username_clean", "email", "hash", "url")
    list_editable = ("username", "email")
    list_display_links = ("__str__",)
    search_fields = ("username",)


@admin.register(AlbumUserMigration)
class AlbumUserMigrationAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "django_user")
    search_fields = ("username",)


@admin.register(AlbumMigration)
class AlbumMigrationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "migrated", "owner", "new_album")
    list_filter = ("migrated",)
    search_fields = ("owner__username", "title", "description")

    def get_queryset(self, request=None):
        base = super().get_queryset(request=request)
        return base.select_related("owner__django_user", "new_album")


@admin.register(PhotoMigration)
class PictureMigrationAdmin(admin.ModelAdmin):
    list_display = ("id", "album", "__str__", "migrated")
    list_editable = ("migrated",)
    list_filter = ("migrated",)
    search_fields = ("owner__username", "album__owner__username", "caption", "title")

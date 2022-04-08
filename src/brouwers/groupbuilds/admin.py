from django.contrib import admin

from .models import GroupBuild, Participant


class InlineParticipant(admin.TabularInline):
    model = Participant
    raw_id_fields = ("user",)


class GroupBuildAdmin(admin.ModelAdmin):
    list_display = ("theme", "status", "category", "start", "end", "num_participants")
    list_editable = ("start", "end", "status")
    list_filter = ("status", "start", "end", "category", "created", "modified")
    search_fields = ("theme", "description", "applicant__username")
    filter_horizontal = ("admins",)
    raw_id_fields = ("applicant",)
    inlines = [InlineParticipant]
    prepopulated_fields = {"slug": ("theme",)}


admin.site.register(GroupBuild, GroupBuildAdmin)

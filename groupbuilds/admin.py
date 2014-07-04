from django.contrib import admin

from .models import GroupBuild, Participant


class InlineParticipant(admin.TabularInline):
    model = Participant


class GroupBuildAdmin(admin.ModelAdmin):
    list_display = ('theme', 'status', 'category', 'start', 'end', 'num_participants')
    list_editable = ('start', 'end', 'status')
    list_filter = ('status', 'start', 'end', 'category', 'created', 'modified')
    search_fields = ('theme', 'description', 'applicant__username')

    inlines = [InlineParticipant]


admin.site.register(GroupBuild, GroupBuildAdmin)

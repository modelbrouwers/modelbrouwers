from datetime import datetime

from django import forms
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.template.defaultfilters import truncatewords
from django.utils.html import format_html
from django.utils.translation import gettext as _

from brouwers.forum_tools.models import Forum

from .models import Category, Project, Vote


def reject(modeladmin, request, queryset):
    queryset.update(rejected=True, last_reviewer=request.user)


reject.short_description = _("Mark nominations as invalid")


def mark_reviewed(modeladmin, request, queryset):
    queryset.update(last_reviewer=request.user, last_review=datetime.now())


mark_reviewed.short_description = _("Mark nominations as reviewed")


def resync_score(modeladmin, request, queryset):
    for nomination in queryset:
        nomination.sync_votes()


resync_score.short_description = _("Re-sync the score based on the cast votes")


class NominationDateFilter(DateFieldListFilter):
    pass
    # def choices(self, cl):
    #     for title, param_dict in self.links:
    #         yield {
    #             'selected': self.date_params == param_dict,
    #             'query_string': cl.get_query_string(
    #                                 param_dict, [self.field_generic]),
    #             'display': title,
    #         }

    # def queryset(self, request, queryset):
    #     return super().queryset(request, queryset)

    #     # if self.value() in DonationStatuses.values:
    #     #     return queryset.filter(status=self.value())
    #     # elif self.value() is None:
    #     #     return queryset.filter(status=self.default_status)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "show_url",
        "reviewed",
        "brouwer",
        "category",
        "nomination_date",
        "rejected",
        "votes",
        "topic_id",
    )
    list_filter = (
        "category",
        ("nomination_date", NominationDateFilter),
    )
    list_select_related = (
        "category",
        "last_reviewer",
    )
    ordering = ("-nomination_date",)
    search_fields = ("name", "nomination_date", "brouwer")

    readonly_fields = ("last_reviewer", "last_review")
    fields = (
        "url",
        "brouwer",
        "name",
        "category",
        "nomination_date",
        "rejected",
        "votes",
        "image",
    ) + readonly_fields

    actions = [reject, mark_reviewed, resync_score]

    def show_url(self, obj) -> str:
        if not obj.topic:
            return _("No topic found!")
        return format_html(
            '<a href="{}">{}</a>',
            obj.topic.get_absolute_url(),
            truncatewords(obj.topic.topic_title, 6),
        )

    show_url.short_description = _("Topic url")

    def reviewed(self, obj):
        return obj.last_reviewer is not None

    reviewed.short_description = _("reviewed?")
    reviewed.boolean = True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.submitter = request.user
        super().save_model(request, obj, form, change)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "submitted")
    raw_id_fields = ("project1", "project2", "project3", "user")
    list_filter = ("submitted", "category")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "forum")
    search_fields = ("name",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "forum":
            field = forms.ModelChoiceField(
                label=db_field.verbose_name,
                required=not db_field.blank,
                queryset=Forum.objects.all(),
            )
            return field
        return super().formfield_for_dbfield(db_field, request, **kwargs)

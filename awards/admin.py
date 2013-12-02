from models import *
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from datetime import datetime

def reject(modeladmin, request, queryset):
    queryset.update(rejected=True, last_reviewer=request.user)
reject.short_description = _('Mark nominations as invalid')

def mark_reviewed(modeladmin, request, queryset):
    queryset.update(last_reviewer=request.user, last_review=datetime.now())
mark_reviewed.short_description = _('Mark nominations as reviewed')


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

    #     import pdb; pdb.set_trace()

    #     return super(NominationDateFilter, self).queryset(request, queryset)

    #     # if self.value() in DonationStatuses.values:
    #     #     return queryset.filter(status=self.value())
    #     # elif self.value() is None:
    #     #     return queryset.filter(status=self.default_status)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_url', 'reviewed', 'brouwer','category','nomination_date', 'nominator', 'rejected', 'votes')
    list_filter = (
        'category',
        ('nomination_date', NominationDateFilter),
    )

    readonly_fields = ('last_reviewer', 'last_review')
    fields = (
        'url',
        'brouwer',
        'name',
        'category',
        'nomination_date',
        'nominator',
        'rejected',
        'votes'
        ) + readonly_fields

    actions = [reject, mark_reviewed]

    def show_url(self, obj):
        return '<a href="%s">topic</a>' % obj.url
    show_url.allow_tags = True
    show_url.short_description = _('Topic url')

    def reviewed(self, obj):
        return obj.last_reviewer is not None
    reviewed.short_description = _('reviewed?')
    reviewed.boolean = True

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_superuser')
UserAdmin.ordering = ['-date_joined', 'username']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

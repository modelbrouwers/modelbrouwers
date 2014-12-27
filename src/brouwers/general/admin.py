from django.conf import settings
from django.contrib import admin

from models import *


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('user', 'forum_nickname')
          }),
        ('Awards', {
            'fields': (('last_vote', 'exclude_from_nomination'), 'categories_voted')
        }),
        ('Secret Santa', {
            'fields': ('secret_santa', ('street','number'),('postal', 'city'),('province','country'), 'preference', 'refuse')
        })
    )

    list_display = ('forum_nickname', 'user', 'full_name', 'exclude_from_nomination', 'last_vote', 'secret_santa')
    list_filter = ('allow_sharing', 'exclude_from_nomination')
    search_fields = ('forum_nickname', 'user__email')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'in_use')
    search_fields = ('question',)


class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer',)


class RegistrationAttemptAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'question_short', 'answer', 'timestamp', 'ip_address', 'success', '_is_banned', 'type_of_visitor')
    list_filter = ('success', 'timestamp', 'type_of_visitor')
    search_fields = ('username',)

    if not settings.DEBUG:
        actions = None


class SoftwareVersionAdmin(admin.ModelAdmin):
    list_diplsay = ('__unicode__', 'start', 'end')


class RedirectAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'path_from', 'path_to')
    list_editable = ('path_from', 'path_to')
    search_fields = ('path_from', 'path_to')


class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'expire', 'h')
    list_filter = ('expire',)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'from_date', 'to_date')
    list_filter = ('language', 'from_date', 'to_date')
    list_editable = ('from_date', 'to_date')
    search_fields = ('text',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RegistrationQuestion, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(RegistrationAttempt, RegistrationAttemptAdmin)
admin.site.register(SoftwareVersion, SoftwareVersionAdmin)
admin.site.register(Redirect, RedirectAdmin)
admin.site.register(PasswordReset, PasswordResetAdmin)
admin.site.register(Announcement, AnnouncementAdmin)